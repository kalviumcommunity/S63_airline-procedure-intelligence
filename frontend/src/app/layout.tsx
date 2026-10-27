import React from 'react';

export const metadata = {
  title: 'SkyOps Intelligence | Ground Procedure Assistant',
  description: 'AI-assisted procedure intelligence for airline ramp and ground operations.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, sans-serif' }}>
        {children}
      </body>
    </html>
  );
}

