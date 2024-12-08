const BASE_URL = "http://localhost:8000";

export interface LoginResponse {
  access_token: string;
}

export interface GenerateResponse {
  id: string;
  link: string;
  text: string;
  status: string;
}

export const login = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error("Invalid credentials");
  }

  return await response.json();
};

export const generateText = async (text: string): Promise<GenerateResponse> => {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${BASE_URL}/documents/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate");
  }

  return await response.json();
};

export const logout = async (): Promise<void> => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    throw new Error("No access token available");
  }

  const response = await fetch(`${BASE_URL}/auth/logout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ access_token: token }),
  });

  if (!response.ok) {
    throw new Error("Failed to logout");
  }

  localStorage.removeItem("access_token");
};