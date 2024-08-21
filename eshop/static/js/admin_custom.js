document.addEventListener('DOMContentLoaded', function() {
    const categorieField = document.getElementById('id_categorie');
    const sousCategorieField = document.getElementById('id_sous_categorie');

    console.log("Inside admin custom JS");  // Vérification que le script est bien chargé

    $(categorieField).on('change', function() {
        const categorieId = $(this).val();
        console.log("Catégorie sélectionnée :", categorieId);  // Vérifie que le changement de catégorie est détecté

        // Efface les sous-catégories actuelles
        $(sousCategorieField).empty().append('<option value="">---------</option>');

        if (!categorieId) return;  // Ne fait rien si aucune catégorie n'est sélectionnée

        // Requête AJAX pour obtenir les sous-catégories
        fetch(`/get_sous_categories/${categorieId}/`)
            .then(response => {
                console.log("Réponse reçue:", response);  // Log de la réponse
                return response.json();
            })
            .then(data => {
                console.log("Données sous-catégories:", data);  // Log des données des sous-catégories

                data.sous_categories.forEach(sousCategorie => {
                    const newOption = new Option(sousCategorie.libelle, sousCategorie.id, false, false);
                    $(sousCategorieField).append(newOption).trigger('change');
                });
            })
            .catch(error => console.error('Erreur lors du chargement des sous-catégories:', error));
    });

    // Recharger Select2 après avoir mis à jour les options
    $(sousCategorieField).select2();
});
