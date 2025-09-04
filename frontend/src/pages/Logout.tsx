import { useMsal } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import type { LogoutProps } from "../types";

// Logout Button Component (used in Dashboard)
export const LogoutButton = ({ onLogout }: LogoutProps) => {
  return (
    <Button onClick={onLogout} variant="outline">
      Logout
    </Button>
  );
};

export const Logout = () => {
  const { instance } = useMsal();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await instance.logoutPopup(); // Logout using popup
      console.log("Logout successful");

      // Clear stored credentials
      sessionStorage.clear();
      localStorage.clear();

      // Redirect to login page
      navigate("/");
    } catch (error) {
      console.error("Logout Error:", error);
    }
  };

  return <Button onClick={handleLogout}>Logout</Button>;
};
