export class APIError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export const handleAPIError = (error: unknown): string => {
  if (error instanceof APIError) {
    return `Error ${error.statusCode}: ${error.message}`;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
};

export const isNetworkError = (error: unknown): boolean => {
  if (error instanceof APIError) {
    return error.statusCode === 0 || error.statusCode >= 500;
  }
  return false;
};
