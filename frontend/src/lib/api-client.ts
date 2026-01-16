import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid, clear token and redirect to login
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  private clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }

  public setToken(token: string | null): void {
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
  }

  public async get<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: any): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // Authentication methods
  public async register(email: string, password: string): Promise<any> {
    return this.post('/auth/register', { email, password });
  }

  public async login(email: string, password: string): Promise<any> {
    return this.post('/auth/login', { email, password });
  }

  // Todo methods
  public async getTodos(params?: {
    completed?: boolean;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{
    todos: any[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }> {
    return this.get('/todos', { params });
  }

  public async getTodo(id: string): Promise<any> {
    return this.get(`/todos/${id}`);
  }

  public async createTodo(data: {
    title: string;
    description?: string;
    priority?: string;
    due_date?: string;
    tag_ids?: string[];
  }): Promise<any> {
    return this.post('/todos', data);
  }

  public async updateTodo(id: string, data: {
    title?: string;
    description?: string;
    completed?: boolean;
    priority?: string;
    due_date?: string;
    tag_ids?: string[];
  }): Promise<any> {
    return this.put(`/todos/${id}`, data);
  }

  public async updateTodoStatus(id: string, completed: boolean): Promise<any> {
    return this.patch(`/todos/${id}/status?completed=${completed}`);
  }

  public async deleteTodo(id: string): Promise<void> {
    return this.delete(`/todos/${id}`);
  }

  // Tag methods
  public async getTags(): Promise<any[]> {
    return this.get('/tags');
  }

  public async createTag(data: { name: string; color?: string }): Promise<any> {
    return this.post('/tags', data);
  }

  public async updateTag(id: string, data: { name?: string; color?: string }): Promise<any> {
    return this.put(`/tags/${id}`, data);
  }

  public async deleteTag(id: string): Promise<void> {
    return this.delete(`/tags/${id}`);
  }
}

export const apiClient = new ApiClient();
