import React, { useState, useEffect  } from 'react';
import {FlatList, View, Text, Image, TouchableOpacity, Modal, StyleSheet, ScrollView } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import BottomNavBar from './components/BottomNavBar';
import Icon from 'react-native-vector-icons/FontAwesome';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { getLatestRecipes } from './tempData'; // Ajustez le chemin
import { SafeAreaView } from 'react-native-safe-area-context';

// Composant distinct pour chaque recette avec son propre état
const RecipeCard = ({ item }) => {
  const [isLiked, setIsLiked] = useState(false); // État pour le bouton "like"
  const [reviewCount, setReviewCount] = useState(item.review_count || 0);  // Compteur de likes
  const [modalVisible, setModalVisible] = useState(false); // Modal d'un item, permet l'affichage d'un recette en particulier



  const toggleLike = () => {
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);
    
    // Mise à jour du compteur en fonction du nouvel état
    setReviewCount(prev => newLikedState ? prev + 1 : Math.max(0, prev - 1));
  };
  
  // Fonction pour afficher les étoiles en fonction de la note
  const renderStars = (rating) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.25 && rating % 1 < 0.75;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
  
    const stars = [];
  
    for (let i = 0; i < fullStars; i++) {
      stars.push(<Icon key={`full-${i}`} name="star" size={20} color="gold" />);
    }
  
    if (hasHalfStar) {
      stars.push(<Icon key="half" name="star-half-full" size={20} color="gold" />);
    }
  
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Icon key={`empty-${i}`} name="star-o" size={20} color="gold" />);
    }
  
    return stars;
  };

  return (    <View>
    <TouchableOpacity style={styles.card} onPress={() => setModalVisible(true)}>
      <Text style={styles.title}>{item.title}</Text>

      <Image
        style={styles.photo}
        source={{ uri: item.photo }}
        resizeMode='cover'
      />

      <View style={styles.ratingContainer}>
        <View style={styles.stars}>
          {renderStars(item.rating)}
          <MaterialCommunityIcons name="alarm" size={40} color="orange" />
          <Text style={styles.text}> {item.prep_time}</Text>

          <TouchableOpacity style={styles.likeButton} onPress={toggleLike}>
            <MaterialCommunityIcons
              name={isLiked ? 'cards-heart' : 'cards-heart-outline'}
              size={40}
              color="red"
            />
          </TouchableOpacity>

          <Text style={styles.text}> {reviewCount}</Text>
        </View>
      </View>
    </TouchableOpacity>

    {/* Le MODAL ici sert a activer une recette specifique quand on clique*/}
    <Modal
      animationType="slide" // de bas en haut
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => setModalVisible(false)}
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <ScrollView>
            <Image source={{ uri: item.photo }} style={styles.modalImage} />

            <Text style={styles.modalTitle}>{item.title}</Text>

            <Text style={styles.modalSubtitle}>Ingrédients :</Text>
            {item.ingredients.map((ingredient, index) => (
              <Text key={index} style={styles.modalText}>• {ingredient}</Text>
            ))}

            <Text style={styles.modalSubtitle}>Étapes :</Text>
            {item.steps.map((step, index) => (
              <Text key={index} style={styles.modalText}>{index + 1}. {step}</Text>
            ))}

            <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
              <Text style={styles.closeButtonText}>Fermer</Text>
            </TouchableOpacity>
          </ScrollView>
        </View>
      </View>
    </Modal>
  </View>
);
};

const recipes = () => {
  const [recettesData, setRecettesData] = useState([]);

  useEffect(() => {
    // Récupérer les données au chargement du composant
    const recipes = getLatestRecipes();
    if (recipes) {
      setRecettesData(recipes);
    }
  }, []);
  return (
    <SafeAreaView style={styles.container}>   
     <Text style={styles.header}>Liste des Recettes</Text>
      <FlatList
        data={recettesData}
        keyExtractor={(item, index) => {  
          if (item._id && typeof item._id !== 'object') {
            return item._id.toString();
          }
          return `recipe-${index}`;
        }}
        renderItem={({ item }) => <RecipeCard item={item} />}
      />

      <BottomNavBar />
  </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3ddbbff',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
    marginTop: 10,
    textAlign: 'center',
    color: '#793d1cff',
  },
  card: {
    marginBottom: 16,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#fffcf7',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#793d1cff',
  },
  subtitle: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 8,
    color: '#793d1cff',
  },
  text: {
    fontSize: 20,
    marginTop: 4,
  },
  photo: {
    width: '100%',
    height: 200,
    marginBottom: 0,
  },
  ratingContainer: {
    flexDirection: 'row',
    marginVertical: 8,
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  stars: {
    flexDirection: 'row',  // Pour aligner les étoiles horizontalement
    alignItems: 'center',
  },
  likeButton: {
    marginHorizontal: 8,
  },
  
  modalContainer: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: 20,
    width: '90%',
    maxHeight: '80%',
    borderRadius: 10,
  },
  modalImage: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    marginBottom: 10,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  modalSubtitle: {
    fontSize: 20,
    fontWeight: '600',
    marginTop: 15,
    marginBottom: 5,
  },
  modalText: {
    fontSize: 16,
    marginVertical: 2,
  },
  closeButton: {
    marginTop: 20,
    backgroundColor: 'orange',
    padding: 10,
    borderRadius: 10,
    alignItems: 'center',
  },
  closeButtonText: {
    color: 'white',
    fontSize: 16,}
});

export default recipes;