
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const Features = () => {
  const features = [
    {
      title: "Ridiculously Fast",
      description: "Django was designed to help developers take applications from concept to completion as quickly as possible.",
      icon: "⚡"
    },
    {
      title: "Reassuringly Secure",
      description: "Django takes security seriously and helps developers avoid many common security mistakes.",
      icon: "🔒"
    },
    {
      title: "Exceedingly Scalable",
      description: "Some of the busiest sites on the web leverage Django's ability to quickly and flexibly scale.",
      icon: "📈"
    },
    {
      title: "Batteries Included",
      description: "Django comes with dozens of extras you can use to handle common web development tasks.",
      icon: "🔋"
    },
    {
      title: "Admin Interface",
      description: "Get a ready-to-use admin interface for managing your content without writing a single line of code.",
      icon: "⚙️"
    },
    {
      title: "ORM",
      description: "Define your data models entirely in Python. You get a rich, dynamic database-access API for free.",
      icon: "🗄️"
    }
  ];

  return (
    <div className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-2 text-center text-django-dark-green">Django Features</h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          Django includes dozens of features that streamline web application development
        </p>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <Card key={index} className="border-t-4 border-t-django-light-green">
              <CardHeader>
                <div className="text-3xl mb-2">{feature.icon}</div>
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Features;
