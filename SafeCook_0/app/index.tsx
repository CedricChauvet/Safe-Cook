import React from 'react';
import { Text, View, StyleSheet } from "react-native";
import { Button } from 'react-native-paper';
import { useRouter } from 'expo-router';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';


export default function Index() {
  const router = useRouter();


  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.title}>SafeCook</Text>
      </View>

      {/* Main Buttons Section */}
      <View style={styles.buttonGroup}>
        {/*<Button
          mode="contained"
          onPress={() => console.log('Accueil cliqué')}
          buttonColor="green"
          labelStyle={styles.buttonLabel}
        >
          Accueil
        </Button>*/}

        <View style={styles.row}>
          {/*<Button
            mode="contained"
            onPress={() => router.push('/photos')}
            buttonColor="green"
            labelStyle={styles.buttonLabel}
          >
            Photos
          </Button>*
          <Button
            mode="contained"
            onPress={() => router.push('/recette')}
            buttonColor="green"
            labelStyle={styles.buttonLabel}
          >
            Recettes
          </Button>
          <Button
            mode="contained"
            onPress={() => console.log('Favoris cliqué')}
            buttonColor="green"
            labelStyle={styles.buttonLabel}
            contentStyle={styles.iconButtonContent}
          >
            <Icon name="heart" size={20} color="white" />
          </Button>*/}
        </View>
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 60,
    backgroundColor: '#f5f5f5',
  },
  header: {
    alignItems: "center",
  },
  title: {
    fontSize: 60,
    color: 'green',
    fontWeight: 'bold',
  },
  dataText: {
    marginTop: 10,
    fontSize: 16,
    color: 'grey',
  },
  buttonGroup: {
    width: "100%",
    alignItems: "center",
  },
  row: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 300,
  },
  buttonLabel: {
    color: 'white',
    fontWeight: 'bold',
  },
  iconButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
});
