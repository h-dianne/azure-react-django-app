export type UserData = {
  username: string;
  email?: string;
  full_name?: string;
  message?: string;
};

export type LogoutProps = {
  onLogout: () => void;
};
