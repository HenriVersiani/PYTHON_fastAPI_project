import { LoginRequest, TokenResponse, User, UserCreate, UserUpdate } from '@/types/api'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    let errorDetails
    try {
      errorDetails = await response.json()
    } catch {
      errorDetails = { detail: response.statusText }
    }
    throw new ApiError(response.status, errorDetails.detail || 'Unknown error', errorDetails)
  }
  return response.json()
}

export const api = {
  login: async (credentials: LoginRequest): Promise<TokenResponse> => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    })
    return handleResponse<TokenResponse>(response)
  },

  createUser: async (user: UserCreate): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user),
    })
    return handleResponse<User>(response)
  },

  getUser: async (userId: number, token?: string): Promise<User> => {
    const headers: HeadersInit = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'GET',
      headers,
    })
    return handleResponse<User>(response)
  },

  listUsers: async (token?: string): Promise<User[]> => {
    const headers: HeadersInit = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await fetch(`${API_BASE_URL}/users/search`, {
      method: 'GET',
      headers,
    })
    return handleResponse<User[]>(response)
  },

  updateUser: async (userId: number, userData: UserUpdate, token?: string): Promise<User> => {
    const headers: HeadersInit = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(userData),
    })
    return handleResponse<User>(response)
  },

  deleteUser: async (userId: number, token?: string): Promise<{ message: string }> => {
    const headers: HeadersInit = {}
    if (token) headers['Authorization'] = `Bearer ${token}`

    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers,
    })
    return handleResponse(response)
  },
}

export { ApiError }
