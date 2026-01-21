'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/contexts/ToastContext';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorBox from '@/components/ErrorBox';
import { validateSignupForm } from '@/lib/signup-validation';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});
  const [backendError, setBackendError] = useState<string | null>(null);
  const router = useRouter();
  const { register } = useAuth();
  const { showToast } = useToast();

  // Helper function to detect duplicate email errors from backend (HTTP 409)
  const isDuplicateEmailError = (error: any): boolean => {
    // Check if Axios error with status code 409 (Conflict)
    return error?.response?.status === 409;
  };

  // Dismiss individual field errors
  const dismissError = (field: 'email' | 'password' | 'confirmPassword') => {
    setFieldErrors(prev => {
      const updated = { ...prev };
      delete updated[field];
      return updated;
    });
  };

  // Dismiss backend error
  const dismissBackendError = () => {
    setBackendError(null);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Validate form using centralized validation utility
    const validation = validateSignupForm({ email, password, confirmPassword });

    if (!validation.isValid) {
      // Set all field errors to display inline error boxes
      setFieldErrors(validation.errors);

      // Also show the first error in toast for backward compatibility
      const firstError = Object.values(validation.errors)[0];
      showToast(firstError, 'error');
      return;
    }

    // Clear any existing errors on successful validation
    setFieldErrors({});
    setBackendError(null);
    setIsLoading(true);

    try {
      await register(email, password);
      showToast('Account created successfully!', 'success');
      router.push('/todos');
    } catch (err) {
      // Check if it's a 409 Conflict error (duplicate email)
      if (isDuplicateEmailError(err)) {
        setBackendError("This email is already registered. Please try another email.");
        showToast("This email is already registered. Please try another email.", 'error');
      } else {
        // Other backend errors - just show toast
        const errorMessage = err instanceof Error ? err.message : 'Registration failed. Please try again.';
        showToast(errorMessage, 'error');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
              sign in to existing account
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-6 animate-fade-in" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* Email Field */}
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  // Clear errors when user starts typing
                  if (fieldErrors.email) {
                    dismissError('email');
                  }
                  if (backendError) {
                    dismissBackendError();
                  }
                }}
                disabled={isLoading}
              />
              {/* Client-side validation error */}
              {fieldErrors.email && (
                <ErrorBox
                  message={fieldErrors.email}
                  onDismiss={() => dismissError('email')}
                />
              )}
              {/* Backend duplicate email error (HTTP 409) */}
              {backendError && (
                <ErrorBox
                  message={backendError}
                  onDismiss={dismissBackendError}
                />
              )}
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Password (min 8 chars, 1 uppercase, 1 lowercase, 1 number)"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  // Clear error when user starts typing
                  if (fieldErrors.password) {
                    dismissError('password');
                  }
                }}
                disabled={isLoading}
              />
              {fieldErrors.password && (
                <ErrorBox
                  message={fieldErrors.password}
                  onDismiss={() => dismissError('password')}
                />
              )}
            </div>

            {/* Confirm Password Field */}
            <div>
              <label htmlFor="confirm-password" className="sr-only">
                Confirm Password
              </label>
              <input
                id="confirm-password"
                name="confirm-password"
                type="password"
                autoComplete="new-password"
                required
                className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                  // Clear error when user starts typing
                  if (fieldErrors.confirmPassword) {
                    dismissError('confirmPassword');
                  }
                }}
                disabled={isLoading}
              />
              {fieldErrors.confirmPassword && (
                <ErrorBox
                  message={fieldErrors.confirmPassword}
                  onDismiss={() => dismissError('confirmPassword')}
                />
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Creating account...</span>
                </>
              ) : (
                'Create account'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
