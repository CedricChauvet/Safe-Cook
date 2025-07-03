// Dans App.tsx ou à la racine de ton projet
import React from 'react';
import { AllergiesProvider } from './contexts/AllergiesContext'; 
import { AuthProvider } from './contexts/AuthContext';
import { Stack } from 'expo-router';

export default function App() {
  return (
    <AuthProvider>
      <AllergiesProvider>
        <Stack
          screenOptions={{
            headerShown: false,
            navigationBarHidden: true
          }}
        />
      </AllergiesProvider>
    </AuthProvider>
  );
}
