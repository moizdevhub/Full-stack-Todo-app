/**
 * Signup Validation Utility
 *
 * This module contains all validation rules and error messages for user signup.
 * It identifies exactly what conditions would block account creation.
 */

export interface ValidationResult {
  isValid: boolean;
  errors: {
    email?: string;
    password?: string;
    confirmPassword?: string;
  };
}

export interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

/**
 * UI-friendly error messages for each validation rule
 */
export const SIGNUP_ERROR_MESSAGES = {
  // Email validation messages
  email: {
    required: 'Email address is required',
    invalid: 'Please enter a valid email address (e.g., user@example.com)',
  },

  // Password validation messages
  password: {
    required: 'Password is required',
    tooShort: 'Password must be at least 8 characters long',
    missingLowercase: 'Password must contain at least one lowercase letter (a-z)',
    missingUppercase: 'Password must contain at least one uppercase letter (A-Z)',
    missingNumber: 'Password must contain at least one number (0-9)',
  },

  // Confirm password validation messages
  confirmPassword: {
    required: 'Please confirm your password',
    mismatch: 'Passwords do not match. Please make sure both passwords are identical',
  },
} as const;

/**
 * Validates email format
 */
export function validateEmail(email: string): string | null {
  if (!email || email.trim() === '') {
    return SIGNUP_ERROR_MESSAGES.email.required;
  }

  // Basic email regex pattern (matches HTML5 email validation)
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(email)) {
    return SIGNUP_ERROR_MESSAGES.email.invalid;
  }

  return null;
}

/**
 * Validates password strength according to backend requirements
 */
export function validatePassword(password: string): string | null {
  if (!password || password.trim() === '') {
    return SIGNUP_ERROR_MESSAGES.password.required;
  }

  // Check minimum length (8 characters)
  if (password.length < 8) {
    return SIGNUP_ERROR_MESSAGES.password.tooShort;
  }

  // Check for at least one lowercase letter
  if (!/[a-z]/.test(password)) {
    return SIGNUP_ERROR_MESSAGES.password.missingLowercase;
  }

  // Check for at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
    return SIGNUP_ERROR_MESSAGES.password.missingUppercase;
  }

  // Check for at least one number
  if (!/[0-9]/.test(password)) {
    return SIGNUP_ERROR_MESSAGES.password.missingNumber;
  }

  return null;
}

/**
 * Validates password confirmation
 */
export function validateConfirmPassword(
  password: string,
  confirmPassword: string
): string | null {
  if (!confirmPassword || confirmPassword.trim() === '') {
    return SIGNUP_ERROR_MESSAGES.confirmPassword.required;
  }

  if (password !== confirmPassword) {
    return SIGNUP_ERROR_MESSAGES.confirmPassword.mismatch;
  }

  return null;
}

/**
 * Validates all signup form fields
 * Returns validation result with specific error messages for each field
 */
export function validateSignupForm(formData: SignupFormData): ValidationResult {
  const errors: ValidationResult['errors'] = {};

  // Validate email
  const emailError = validateEmail(formData.email);
  if (emailError) {
    errors.email = emailError;
  }

  // Validate password
  const passwordError = validatePassword(formData.password);
  if (passwordError) {
    errors.password = passwordError;
  }

  // Validate confirm password
  const confirmPasswordError = validateConfirmPassword(
    formData.password,
    formData.confirmPassword
  );
  if (confirmPasswordError) {
    errors.confirmPassword = confirmPasswordError;
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}

/**
 * Gets all password requirements as a list (useful for displaying requirements to users)
 */
export function getPasswordRequirements(): string[] {
  return [
    'At least 8 characters long',
    'At least one lowercase letter (a-z)',
    'At least one uppercase letter (A-Z)',
    'At least one number (0-9)',
  ];
}

/**
 * Checks which password requirements are met (useful for real-time feedback)
 */
export function checkPasswordRequirements(password: string) {
  return {
    hasMinLength: password.length >= 8,
    hasLowercase: /[a-z]/.test(password),
    hasUppercase: /[A-Z]/.test(password),
    hasNumber: /[0-9]/.test(password),
  };
}
