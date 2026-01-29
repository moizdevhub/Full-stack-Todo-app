/**
 * Better Auth integration service
 * Handles JWT token management and user authentication
 */

/**
 * Get the current JWT token from Better Auth
 * @returns JWT token string or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Better Auth stores tokens in cookies by default
    // We'll retrieve it from the session
    const response = await fetch('/api/auth/session', {
      credentials: 'include',
    });

    if (!response.ok) {
      return null;
    }

    const session = await response.json();
    return session?.token || null;
  } catch (error) {
    console.error('Failed to get auth token:', error);
    return null;
  }
}

/**
 * Extract user_id from JWT token
 * @param token JWT token string
 * @returns User UUID from sub claim or null if invalid
 */
export function getUserIdFromToken(token: string): string | null {
  try {
    // JWT format: header.payload.signature
    const parts = token.split('.');
    if (parts.length !== 3) {
      return null;
    }

    // Decode payload (base64url)
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));

    // Extract user_id from sub claim
    return payload.sub || null;
  } catch (error) {
    console.error('Failed to decode JWT token:', error);
    return null;
  }
}

/**
 * Get the current authenticated user's ID
 * @returns User UUID or null if not authenticated
 */
export async function getCurrentUserId(): Promise<string | null> {
  const token = await getAuthToken();
  if (!token) {
    return null;
  }
  return getUserIdFromToken(token);
}

/**
 * Check if user is authenticated
 * @returns true if user has valid session
 */
export async function isAuthenticated(): Promise<boolean> {
  const token = await getAuthToken();
  return token !== null;
}

/**
 * Sign out the current user
 */
export async function signOut(): Promise<void> {
  try {
    await fetch('/api/auth/signout', {
      method: 'POST',
      credentials: 'include',
    });
  } catch (error) {
    console.error('Failed to sign out:', error);
  }
}
