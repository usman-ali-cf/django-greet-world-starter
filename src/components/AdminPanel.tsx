
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const AdminPanel = () => {
  return (
    <Card className="border-django-dark-green">
      <CardHeader className="bg-django-dark-green text-white">
        <CardTitle>Django Administration</CardTitle>
        <CardDescription className="text-django-light-text">Site Administration</CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="grid gap-4">
          <div>
            <h3 className="text-lg font-medium mb-2">Authentication and Authorization</h3>
            <ul className="space-y-1 text-sm">
              <li>👤 Users</li>
              <li>👥 Groups</li>
              <li>🔑 Permissions</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-medium mb-2">Content Management</h3>
            <ul className="space-y-1 text-sm">
              <li>📝 Blog posts</li>
              <li>💬 Comments</li>
              <li>🏷️ Categories</li>
            </ul>
          </div>
          
          <div className="mt-4">
            <Button className="bg-django-light-green hover:bg-django-dark-green text-white">
              Log In
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AdminPanel;
