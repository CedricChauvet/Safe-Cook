import React from 'react';

import {
  Modal,
  StyleSheet,
  Text,
  TouchableOpacity,
  TouchableWithoutFeedback,
  View
} from 'react-native';
import { useAllergies } from './contexts/AllergiesContext';

/**
 * Interface définissant les props acceptées par le composant AllergiesModal.
 */
interface AllergiesModalProps {
  visible: boolean;         // Contrôle la visibilité du modal
  onClose: () => void;      // Fonction appelée pour fermer le modal
  title: string;            // Titre affiché dans l'en-tête du modal
  children?: React.ReactNode; // (Optionnel) Contenu personnalisé inséré dans le modal
}

// Liste des allergies disponibles à afficher sous forme de boutons
const allergieOptions = ['Gluten', 'Lactose', 'Arachides', 'Végétarien'];

/**
 * Composant modal permettant à l'utilisateur de choisir ses préférences alimentaires ou allergies.
 */
const AllergiesModal: React.FC<AllergiesModalProps> = ({
  visible,
  onClose,
  title,
  children,
}) => {
  // Récupère les allergies et la fonction de toggle depuis le contexte global
  const { allergies, toggleAllergie } = useAllergies();

  /**
   * Fonction utilitaire pour générer dynamiquement un bouton de toggle pour une allergie donnée.
   * @param label - Nom de l'allergie (clé du contexte)
   * @returns JSX d'un bouton tactile affichant l'état activé/désactivé
   */
  const renderToggle = (label: string) => {
    const isActive = allergies[label]; // Vérifie si l'allergie est active
    return (
      <TouchableOpacity
        key={label}
        style={[
          styles.toggleButton,
          isActive ? styles.toggleButtonActive : styles.toggleButtonInactive,
        ]}
        onPress={() => toggleAllergie(label)} // Inverse l'état de l'allergie dans le contexte
      >
        <Text
          style={[
            styles.toggleButtonText,
            isActive ? styles.toggleTextActive : styles.toggleTextInactive,
          ]}
        >
          {label}
        </Text>
      </TouchableOpacity>
    );
  };

  /**
   * Composant visuel retourné, affichant :
   * - un fond semi-transparent (TouchableWithoutFeedback pour fermer)
   * - une boîte modale centrée contenant le titre, les enfants, et les toggles
   */
  return (
    <Modal animationType="slide" transparent visible={visible} onRequestClose={onClose}>
      {/* Ferme le modal si on touche l'extérieur */}
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay} />
      </TouchableWithoutFeedback>

      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          {/* En-tête du modal avec le titre */}
          <View style={styles.header}>
            <Text style={styles.headerText}>{title}</Text>
          </View>

          {/* Contenu principal du modal */}
          <View style={styles.contentContainer}>
            {children}

            {/* Génère dynamiquement 2 boutons par ligne */}
            {Array.from({ length: allergieOptions.length / 2 }).map((_, rowIndex) => (
              <View key={rowIndex} style={styles.toggleContainer}>
                {renderToggle(allergieOptions[rowIndex * 2])}
                {renderToggle(allergieOptions[rowIndex * 2 + 1])}
              </View>
            ))}
          </View>
        </View>
      </View>
    </Modal>
  );
};


const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    width: '80%',
    backgroundColor: 'white',
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f8f8',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerText: {
    fontWeight: 'bold',
    fontSize: 18,
  },
  contentContainer: {
    padding: 15,
  },
  toggleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 10,
  },
  toggleButton: {
    flex: 1,
    padding: 10,
    marginHorizontal: 5,
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  toggleButtonActive: {
    backgroundColor: '#4CAF50',
  },
  toggleButtonInactive: {
    backgroundColor: '#f1f1f1',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  toggleButtonText: {
    fontWeight: '500',
  },
  toggleTextActive: {
    color: 'white',
  },
  toggleTextInactive: {
    color: '#666',
  },
});

export default AllergiesModal;