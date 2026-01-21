# Signup Validation Rules & Error Messages

This document lists all validation rules that prevent account creation in the Todo app, along with UI-friendly error messages for each condition.

---

## 📋 Complete List of Validation Rules

### 1. **Email Validation**

| Rule | Condition | Error Message |
|------|-----------|---------------|
| **Required** | Email field is empty | "Email address is required" |
| **Valid Format** | Email doesn't match pattern `user@domain.com` | "Please enter a valid email address (e.g., user@example.com)" |

**Technical Implementation:**
- HTML5 `type="email"` attribute (browser-native validation)
- Regex pattern: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`

---

### 2. **Password Validation**

| Rule | Condition | Error Message |
|------|-----------|---------------|
| **Required** | Password field is empty | "Password is required" |
| **Minimum Length** | Password has fewer than 8 characters | "Password must be at least 8 characters long" |
| **Lowercase Letter** | Password doesn't contain any lowercase letter (a-z) | "Password must contain at least one lowercase letter (a-z)" |
| **Uppercase Letter** | Password doesn't contain any uppercase letter (A-Z) | "Password must contain at least one uppercase letter (A-Z)" |
| **Number** | Password doesn't contain any digit (0-9) | "Password must contain at least one number (0-9)" |

**Technical Implementation:**
- Minimum length check: `password.length < 8`
- Lowercase regex: `/[a-z]/`
- Uppercase regex: `/[A-Z]/`
- Number regex: `/[0-9]/`

**Valid Password Examples:**
- ✅ `Password123`
- ✅ `MySecure1Pass`
- ✅ `Test1234`

**Invalid Password Examples:**
- ❌ `pass123` (missing uppercase)
- ❌ `PASSWORD123` (missing lowercase)
- ❌ `Password` (missing number)
- ❌ `Pass1` (too short, less than 8 characters)

---

### 3. **Confirm Password Validation**

| Rule | Condition | Error Message |
|------|-----------|---------------|
| **Required** | Confirm password field is empty | "Please confirm your password" |
| **Match** | Confirm password doesn't match password field | "Passwords do not match. Please make sure both passwords are identical" |

**Technical Implementation:**
- Direct string comparison: `password !== confirmPassword`

---

## 🔧 Usage Guide

### Using the Validation Utility

The validation utility is located at: `frontend/src/lib/signup-validation.ts`

#### **Option 1: Validate Individual Fields**

```typescript
import { validateEmail, validatePassword, validateConfirmPassword } from '@/lib/signup-validation';

// Validate email
const emailError = validateEmail('user@example.com');
if (emailError) {
  console.log(emailError); // Shows specific error message
}

// Validate password
const passwordError = validatePassword('MyPass123');
if (passwordError) {
  console.log(passwordError); // Shows specific error message
}

// Validate confirm password
const confirmError = validateConfirmPassword('MyPass123', 'MyPass123');
if (confirmError) {
  console.log(confirmError); // Shows specific error message
}
```

#### **Option 2: Validate Entire Form**

```typescript
import { validateSignupForm } from '@/lib/signup-validation';

const result = validateSignupForm({
  email: 'user@example.com',
  password: 'MyPass123',
  confirmPassword: 'MyPass123'
});

if (!result.isValid) {
  console.log(result.errors);
  // {
  //   email?: "Error message",
  //   password?: "Error message",
  //   confirmPassword?: "Error message"
  // }
}
```

#### **Option 3: Real-time Password Strength Indicator**

```typescript
import { checkPasswordRequirements, getPasswordRequirements } from '@/lib/signup-validation';

// Get list of requirements to display
const requirements = getPasswordRequirements();
// Returns:
// [
//   "At least 8 characters long",
//   "At least one lowercase letter (a-z)",
//   "At least one uppercase letter (A-Z)",
//   "At least one number (0-9)"
// ]

// Check which requirements are met (for real-time feedback)
const status = checkPasswordRequirements('MyPass');
// Returns:
// {
//   hasMinLength: false,    // Only 6 characters
//   hasLowercase: true,     // Has 'a', 's', 's'
//   hasUppercase: true,     // Has 'M', 'P'
//   hasNumber: false        // No numbers
// }
```

---

## 📝 Error Messages Object

All error messages are available as a constant object:

```typescript
import { SIGNUP_ERROR_MESSAGES } from '@/lib/signup-validation';

// Access specific messages
SIGNUP_ERROR_MESSAGES.email.required
// "Email address is required"

SIGNUP_ERROR_MESSAGES.password.tooShort
// "Password must be at least 8 characters long"

SIGNUP_ERROR_MESSAGES.confirmPassword.mismatch
// "Passwords do not match. Please make sure both passwords are identical"
```

---

## 🎯 Integration Example

Here's how to integrate the validation utility into a signup form:

```typescript
'use client';

import { useState, FormEvent } from 'react';
import { validateSignupForm } from '@/lib/signup-validation';

export default function SignupForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validate form
    const validation = validateSignupForm({ email, password, confirmPassword });

    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    // Proceed with registration...
    try {
      await register(email, password);
    } catch (error) {
      // Handle API errors
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {errors.email && <p className="error">{errors.email}</p>}

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errors.password && <p className="error">{errors.password}</p>}

      <input
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}

      <button type="submit">Sign Up</button>
    </form>
  );
}
```

---

## 🚫 What Blocks Account Creation

An account **CANNOT** be created if:

1. ❌ Email is empty or invalid format
2. ❌ Password is less than 8 characters
3. ❌ Password is missing a lowercase letter
4. ❌ Password is missing an uppercase letter
5. ❌ Password is missing a number
6. ❌ Confirm password doesn't match password
7. ❌ Any required field is empty

---

## 📍 Current Implementation Location

The existing validation logic is in:
- **File:** `frontend/src/app/register/page.tsx`
- **Lines:** 22-47 (validation logic)
- **Method:** Inline validation in `handleSubmit` function

The new validation utility provides:
- ✅ Reusable validation functions
- ✅ Centralized error messages
- ✅ TypeScript type safety
- ✅ Easy to test and maintain
- ✅ Can be used across multiple forms

---

## 🔄 Migration Path (Optional)

To use the new validation utility in the existing register page:

1. Import the validation function:
   ```typescript
   import { validateSignupForm } from '@/lib/signup-validation';
   ```

2. Replace the inline validation (lines 22-47) with:
   ```typescript
   const validation = validateSignupForm({ email, password, confirmPassword });

   if (!validation.isValid) {
     const firstError = Object.values(validation.errors)[0];
     showToast(firstError, 'error');
     return;
   }
   ```

This maintains the same UX while using the centralized validation utility.
