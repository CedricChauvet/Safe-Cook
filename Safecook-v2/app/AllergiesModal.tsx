// Ce modal permet de choisir les allergie utilisateur, 

import React from 'react';
import { Modal, View, Text, TouchableOpacity, TouchableWithoutFeedback, StyleSheet} from 'react-native';

// Import de la variable de context, sauvegardée en dur  avec AllergiesContext.tsx
import { useAllergies } from './contexts/AllergiesContext'; 


// Définition de l'interface pour les propriétés (props) du composant AllergiesModal
interface AllergiesModalProps {
  // 'visible' indique si le modal est visible ou non (true = affiché, false = caché)
  visible: boolean;
  // 'onClose' est une fonction appelée pour fermer le modal
  onClose: () => void;
  // 'title' est le texte du titre affiché en haut du modal
  title: string;
  // 'children' permet d'insérer du contenu personnalisé à l'intérieur du modal (optionnel)
  children?: React.ReactNode;
}

// L'objet AllergiesModal est le modal qui va permettre de choisir les allergies de l'utilisateur
// l'objet herite de AllergiesModalProps
const AllergiesModal: React.FC<AllergiesModalProps> = ({
  visible,
  onClose,
  title,
  children,
}) => {

  // déclaration des varialble de context
  const { allergies, toggleAllergie } = useAllergies(); 

  const isToggleActive1 = allergies.Gluten;
  const isToggleActive2 = allergies.Lactose;
  const isToggleActive3 = allergies.Arachides;
  const isToggleActive4 = allergies.Végétarien;

  const handleToggle1 = () => toggleAllergie('Gluten');
  const handleToggle2 = () => toggleAllergie('Lactose');
  const handleToggle3 = () => toggleAllergie('Arachides');
  const handleToggle4 = () => toggleAllergie('Végétarien');

  return (
    <Modal animationType="slide" transparent={true} visible={visible} onRequestClose={onClose}>

      {/* close AllergiesModal si on touche l'ecran */}
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay} />
      </TouchableWithoutFeedback>

      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          {/* Header du Modal avec le titre */}
          <View style={styles.header}>
            <Text style={styles.headerText}>{title}</Text>
          </View>
          
            {/*  children est tout le contenu que tu veux afficher à l'intérieur du Modal  */}  
          <View style={styles.contentContainer}>
            {children}

            {/* Toggle  4   Buttons Row */}
            <View style={styles.toggleContainer}>
              <TouchableOpacity
                style={[styles.toggleButton, isToggleActive1 ? styles.toggleButtonActive : styles.toggleButtonInactive]}
                onPress={handleToggle1}
              >
                <Text
                  style={[styles.toggleButtonText, isToggleActive1 ? styles.toggleTextActive : styles.toggleTextInactive]}
                >
                  Gluten
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.toggleButton, isToggleActive2 ? styles.toggleButtonActive : styles.toggleButtonInactive]}
                onPress={handleToggle2}
              >
                <Text
                  style={[styles.toggleButtonText, isToggleActive2 ? styles.toggleTextActive : styles.toggleTextInactive]}
                >
                  Lactose
                </Text>
              </TouchableOpacity>
            </View>

            <View style={styles.toggleContainer}>
              <TouchableOpacity
                style={[styles.toggleButton, isToggleActive3 ? styles.toggleButtonActive : styles.toggleButtonInactive]}
                onPress={handleToggle3}
              >
                <Text
                  style={[styles.toggleButtonText, isToggleActive3 ? styles.toggleTextActive : styles.toggleTextInactive]}
                >
                  Arachides
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.toggleButton, isToggleActive4 ? styles.toggleButtonActive : styles.toggleButtonInactive]}
                onPress={handleToggle4}
              >
                <Text
                  style={[styles.toggleButtonText, isToggleActive4 ? styles.toggleTextActive : styles.toggleTextInactive]}
                >
                  Végétarien
                </Text>
              </TouchableOpacity>
            </View>
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
  closeIcon: {
    padding: 5,
  },
  closeIconText: {
    fontSize: 18,
    fontWeight: 'bold',
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
