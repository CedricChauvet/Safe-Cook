import React, { useState } from 'react';
import { View, Text, FlatList, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import BottomNavBar from './components/BottomNavBar';
import Icon from 'react-native-vector-icons/FontAwesome';
import { MaterialCommunityIcons } from '@expo/vector-icons';

// Composant distinct pour chaque recette avec son propre état
const RecipeCard = ({ item }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [reviewCount, setReviewCount] = useState(item.review_count || 0);

  const toggleLike = () => {
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);
    
    // Mise à jour du compteur en fonction du nouvel état
    setReviewCount(prev => newLikedState ? prev + 1 : Math.max(0, prev - 1));
  };

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

  return (
    <View style={styles.card}>
      <Text style={styles.title}>{item.title}</Text>

      <Image
        style={styles.photo}
        source={{ uri: item.photo }}
        resizeMode='cover'
      />
      {/* Informations sur la recette */}
      <View style={styles.ratingContainer}>
        <View style={styles.stars}>
          {renderStars(item.rating)}

          <MaterialCommunityIcons 
            
            name="alarm" 
            size={40} 
            color="orange" 
          />
          <Text style={styles.text}> {item.prep_time}</Text>
        
          <TouchableOpacity
            style={styles.likeButton}
            onPress={toggleLike}
          >
            <MaterialCommunityIcons
              name={isLiked ? 'cards-heart' : 'cards-heart-outline'}
              size={40}
              color="red"
            />
          </TouchableOpacity>
          <Text style={styles.text}> {reviewCount}</Text>
        </View>
      </View>
    </View>
  );
};

const Recipes = () => {
  const params = useLocalSearchParams();
  // Analyser les recettes à partir des paramètres
  const recettesData = params.recettes ? JSON.parse(params.recettes) : [];

  return (
    <View style={styles.container}>
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
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
  }
});

export default Recipes;