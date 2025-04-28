import { Alert } from "react-native";

// Fichier pour stocker temporairement des données entre les composants
export let latestRecipesData = null;

export const setLatestRecipes = (data) => {
  latestRecipesData = data;
};

export const getLatestRecipes = () => {
  return latestRecipesData;
};