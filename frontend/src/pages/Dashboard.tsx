import { useEffect, useState } from "react";
import axios from "axios";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../config/authConfig";
import { useNavigate } from "react-router-dom";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LogoutButton } from "./Logout";
import type { UserData } from "../types";

export const Dashboard = () => {
  const { instance, accounts } = useMsal();
  const navigate = useNavigate();
  const [userData, setUserData] = useState<UserData | null>(null);

  useEffect(() => {
    const storedAccount = JSON.parse(
      localStorage.getItem("activeAccount") || "null"
    );
    const accountToUse = accounts.length > 0 ? accounts[0] : storedAccount;

    if (accountToUse) {
      instance.setActiveAccount(accountToUse);
      localStorage.setItem("activeAccount", JSON.stringify(accountToUse));

      const cachedToken = sessionStorage.getItem("accessToken");

      if (cachedToken) {
        fetchDashboardData(cachedToken);
      } else {
        instance
          .acquireTokenSilent({
            ...loginRequest,
            account: accountToUse
          })
          .then((tokenResponse) => {
            sessionStorage.setItem("accessToken", tokenResponse.accessToken);
            fetchDashboardData(tokenResponse.accessToken);
          })
          .catch((error) => {
            console.error("Token Error:", error);
            navigate("/");
          });
      }
    } else {
      navigate("/");
    }
  }, [instance, accounts, navigate]);

  const fetchDashboardData = (token: string) => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
    axios
      .get(`${apiBaseUrl}api/v1/dashboard/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => console.error("API Error:", error));
  };

  const handleLogout = () => {
    localStorage.removeItem("activeAccount");
    sessionStorage.removeItem("accessToken");
    instance.logoutRedirect().then(() => {
      navigate("/");
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <LogoutButton onLogout={handleLogout} />
        </div>

        <Card>
          <CardHeader>
            <CardTitle>User Information</CardTitle>
            <CardDescription>
              Your account details from Azure AD
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {userData ? (
              <>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">Username</Badge>
                    <span className="font-medium">{userData.username}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">Email</Badge>
                    <span className="font-medium">
                      {userData.email || "Not Available"}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">Full Name</Badge>
                    <span className="font-medium">
                      {userData.full_name || "Not Available"}
                    </span>
                  </div>
                </div>
                <Alert>
                  <AlertDescription>{userData.message}</AlertDescription>
                </Alert>
              </>
            ) : (
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Skeleton className="h-6 w-20" />
                  <Skeleton className="h-6 w-40" />
                </div>
                <div className="flex items-center space-x-2">
                  <Skeleton className="h-6 w-20" />
                  <Skeleton className="h-6 w-40" />
                </div>
                <div className="flex items-center space-x-2">
                  <Skeleton className="h-6 w-20" />
                  <Skeleton className="h-6 w-40" />
                </div>
                <Skeleton className="h-12 w-full" />
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
