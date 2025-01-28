#!/bin/bash
 
# Sauvegarde du package.json existant
echo "🔄 Sauvegarde du package.json actuel..."
cp package.json package.json.backup
echo "✅ Sauvegarde créée : package.json.backup"

# Fonction pour vérifier si la dernière commande a réussi
check_error() {
    if [ $? -ne 0 ]; then
        echo "❌ Une erreur est survenue. Restauration du package.json original..."
        cp package.json.backup package.json
        exit 1
    fi
}

# Installation des modules
echo "🚀 Début de l'installation des modules..."

modules=(
    "@react-native-async-storage/async-storage@1.23.1"
    "@react-native-picker/picker@2.9.0"
    "expo-blur@~14.0.3"
    "expo-camera@~16.0.14"
    "expo-font@~13.0.3"
    "expo-haptics@~14.0.1"
    "expo-linking@~7.0.4"
    "expo-router@~4.0.17"
    "expo-splash-screen@~0.29.21"
    "expo-status-bar@~2.0.1"
    "expo-symbols@~0.2.1"
    "expo-system-ui@~4.0.7"
    "expo-web-browser@~14.0.2"
    "react-native@0.76.6"
    "jest-expo@~52.0.3"
)

for module in "${modules[@]}"
do
    echo "📦 Installation de $module"
    npm install "$module" --save
    check_error
done

# Nettoyage du cache npm
echo "🧹 Nettoyage du cache npm..."
npm cache clean --force
check_error

# Vérification des installations
echo "🔍 Vérification des installations..."
npm ls "${modules[@]/%/@*}" 2>/dev/null

echo "✨ Installation terminée avec succès!"
echo "📝 Note: Une sauvegarde de votre package.json original a été créée (package.json.backup)"
