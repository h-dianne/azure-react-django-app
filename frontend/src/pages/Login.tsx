import { useMsal } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";

import { loginRequest } from "../config/authConfig";

export const Login = () => {
  const { instance } = useMsal();
  const navigate = useNavigate();

  const handleLogin = () => {
    instance
      .loginPopup(loginRequest)
      .then(() => {
        navigate("/dashboard");
      })
      .catch((error) => console.error("Login failed: ", error));
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Welcome to the App</CardTitle>
          <CardDescription>
            Sign in with your Azure AD account to continue
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button onClick={handleLogin} className="w-full" size="lg">
            Login with Azure AD
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};
