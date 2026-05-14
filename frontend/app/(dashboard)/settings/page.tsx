"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { getToken, removeToken } from "@/lib/auth";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
}

export default function SettingsPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    apiClient<UserProfile>("/api/v1/auth/me", { token })
      .then(setProfile)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  const handleLogout = () => {
    removeToken();
    router.push("/login");
  };

  return (
    <div className="space-y-6">
      <h1 className="font-heading text-2xl text-foreground">Settings</h1>

      {loading ? (
        <div className="h-24 animate-pulse rounded bg-hover" />
      ) : profile ? (
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <p className="font-body text-xs text-secondary">Name</p>
                <p className="font-body text-sm text-foreground mt-1">{profile.full_name}</p>
              </div>
              <div>
                <p className="font-body text-xs text-secondary">Email</p>
                <p className="font-body text-sm text-foreground mt-1">{profile.email}</p>
              </div>
              <div>
                <p className="font-body text-xs text-secondary">User ID</p>
                <p className="font-fira-code text-xs text-secondary mt-1">{profile.id.slice(0, 8)}...</p>
              </div>
              <div>
                <p className="font-body text-xs text-secondary">Status</p>
                <div className="mt-1">
                  <Badge variant={profile.is_active ? "success" : "failed"}>
                    {profile.is_active ? "ACTIVE" : "INACTIVE"}
                  </Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="rounded border border-red-light/30 bg-red/10 p-4 text-red-light">
          Could not load profile. Please try logging in again.
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="font-body text-sm text-secondary">
            Manage your account settings and session.
          </p>
          <Button variant="destructive" className="mt-4" onClick={handleLogout}>
            Sign Out
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="font-body text-sm text-secondary">
            SalesPredict AI CRM v0.1.0 — AI-powered sales forecasting with XGBoost
            and real-time dashboards.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
