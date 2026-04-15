// API Types
export interface User {
  id: number
  name: string
  email: string
  role_id: number
}

export interface UserCreate {
  name: string
  email: string
  password: string
  role_id?: number
}

export interface UserUpdate {
  name?: string
  email?: string
  role_id?: number
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiErrorResponse {
  detail: string | Record<string, string[]>
}
