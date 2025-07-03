import React from 'react';
import {
  Modal,
  StyleSheet,
  Text,
  TouchableOpacity,
  TouchableWithoutFeedback,
  View,
} from 'react-native';
import { useAllergies } from './contexts/AllergiesContext';

interface AllergiesModalProps {
  visible: boolean;
  onClose: () => void;
  title: string;
  children?: React.ReactNode;
  currentUserId: number; // on peut éventuellement supprimer ce prop si non utilisé
}

const allergieOptions = [
  { label: 'Gluten', id: 1 },
  { label: 'Lactose', id: 2 },
  { label: 'Arachides', id: 3 },
  { label: 'Végétarien', id: 4 },
];

const AllergiesModal: React.FC<AllergiesModalProps> = ({
  visible,
  onClose,
  title,
  children,
}) => {
  const { allergies, toggleAllergie } = useAllergies();

  const renderToggle = (label: keyof typeof allergies) => {
    const isActive = allergies[label];

    return (
      <TouchableOpacity
        key={label}
        style={[
          styles.toggleButton,
          isActive ? styles.toggleButtonActive : styles.toggleButtonInactive,
        ]}
        onPress={() => {
          console.log('🟢 Toggle pressed:', label);
          toggleAllergie(label);
        }}
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

  return (
    <Modal animationType="slide" transparent visible={visible} onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay} />
      </TouchableWithoutFeedback>

      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          <View style={styles.header}>
            <Text style={styles.headerText}>{title}</Text>
          </View>

          <View style={styles.contentContainer}>
            {children}

            {/* Affiche les boutons 2 par 2 */}
            {Array.from({ length: allergieOptions.length / 2 }).map((_, rowIndex) => (
              <View key={rowIndex} style={styles.toggleContainer}>
                {renderToggle(allergieOptions[rowIndex * 2].label as keyof typeof allergies)}
                {renderToggle(allergieOptions[rowIndex * 2 + 1].label as keyof typeof allergies)}
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
    flex: 1,
    backgroundColor: '#00000066',
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 20,
  },
  modalView: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    elevation: 5,
    width: '100%',
  },
  header: {
    marginBottom: 10,
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  contentContainer: {
    marginTop: 10,
  },
  toggleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 8,
  },
  toggleButton: {
    flex: 1,
    paddingVertical: 10,
    marginHorizontal: 5,
    borderRadius: 8,
    borderWidth: 1,
    alignItems: 'center',
  },
  toggleButtonActive: {
    backgroundColor: '#4caf50',
    borderColor: '#388e3c',
  },
  toggleButtonInactive: {
    backgroundColor: '#fff',
    borderColor: '#ccc',
  },
  toggleButtonText: {
    fontSize: 16,
  },
  toggleTextActive: {
    color: 'white',
    fontWeight: 'bold',
  },
  toggleTextInactive: {
    color: '#333',
  },
});

export default AllergiesModal;
