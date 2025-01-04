        window.onload = () => genere_grille(id_game);
        tour_joueur();
        //fonction de génération de l'image de grille : 
        async function genere_grille(id_game) {

            const response = await fetch("/generate", {
                method: "POST",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ number: id_game }),
            });

            const result = await response.json();

            if (response.ok) {
                // Met a jour l'image
                document.getElementById("output-image").src = result.image_url + '?' + new Date().getTime();
            } else {
                alert(result.error || "Une erreur a eu lieu");
            }
        }
        async function tour_joueur() {
            const response = await fetch("/joueur", {
                method: "POST",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ number: id_game }),
            });

            const result = await response.json();

            if (response.ok) {
<<<<<<< Updated upstream
                document.getElementById("couleur_joueur").textContent = result.joueur;
                const couleurElement = document.getElementById('couleur_joueur');
                if (result.couleur == 'B') {
                    couleurElement.style.color = 'white';
                    couleurElement.style.backgroundColor = 'blue';
                }
                else if (result.couleur == 'Y') {
                    couleurElement.style.color = 'black';
                    couleurElement.style.backgroundColor= 'yellow';
                }
                else if (result.couleur == 'R') {
                    couleurElement.style.color = 'white';
                    couleurElement.style.backgroundColor = 'red';
                }
                else if (result.couleur == 'G') {
                    couleurElement.style.color = 'white';
                    couleurElement.style.backgroundColor = 'green';
                }
=======
                // Met a jour l'image
                document.getElementById("couleur_joueur").textContent = result.joueur;
>>>>>>> Stashed changes
            } else {
                alert(result.error || "Une erreur a eu lieu pour le joueur");
            }
        }
        function updategrille(){
            genere_grille(id_game)
        }
        
        function fin_de_partie() {
            console.log("partie finie");
            window.location.href = `/fin_de_partie/${id_game}`;
        }
        
        // Sélectionne toutes les images et applique la fonction glisseElement à chacune
        let elements = document.querySelectorAll('.posi');
        elements.forEach(element => {
            glisseElement(element);
        });

        var elementReel = ""
        var retourne = 1
        var rotation = 0
        var carreX = 0
        var carreY = 0
        let envoie = null

        async function envoieValeur(carrX, carrY, retourne, rotation , element) {
            console.log("retourne et rotation :", retourne, rotation)
            const response = await fetch("/submit22", { 
                method: "POST",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ carrX: carrX, carrY: carrY , retourne : retourne , rotation : rotation , element : element , color : color , id_game :id_game}),
            });
        
            if (response.ok) {
                console.log("reponseok")
                const result = await response.json();
                if (result.status == "coup valide"){
                    console.log("coup valide");
                    genere_grille(id_game);
                    var nonid = document.getElementById(element);
                    console.log("nb_joueur",nb_joueur)
                    nonid.remove();
                    if (nb_joueur == 1 || nb_joueur == 2){
                        console.log("changement de joueur")
                        location.reload()
                    }

                console.log('Réponse du serveur:', result);}
                else if (result.status == "pas le bon tour"){
                    setTimeout(function() {
                        document.getElementById('tempo').classList.add('visible'); // Ajouter la classe 'visible' pour rendre l'élément visible avec animation
                    }, 10); 
                    setTimeout(function() {
                        document.getElementById('tempo').classList.remove('visible'); // Enlève la classe 'visible' pour rendre l'élément visible avec animation
                    }, 3000); 
                }
                else if (result.status == "coup interdit"){
                    // Après avoir ajouté l'élément, ajouter la classe 'visible' après un court délai pour déclencher l'animation
                    setTimeout(function() {
                        document.getElementById('temporaire').classList.add('visible'); // Ajouter la classe 'visible' pour rendre l'élément visible avec animation
                    }, 10); 
                    setTimeout(function() {
                        document.getElementById('temporaire').classList.remove('visible'); // Enlève la classe 'visible' pour rendre l'élément visible avec animation
                    }, 3000); 
                }
                }
             else {
                console.error('Erreur dans la réponse:', response.status);
            }
        }

        function glisseElement(element) {
            let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
            let doubleClic = false;
            element.dataset.flip = "1";
            element.dataset.rotation = "0";
            // Quand la souris sélectionne l'image, on lance une nouvelle fonction
            element.addEventListener('dblclick',function (event){
                document.addEventListener('contextmenu', function(event) {
                    event.preventDefault();
                })
                flip(element.querySelector("img"))
                doubleClic = true;
            })
            element.querySelector("img").onmousedown = function(event){
                document.addEventListener('contextmenu', function(event) {
                    event.preventDefault();
                })
                if (doubleClic) {
                    doubleClic = false;
                    return;
                }
                else if (event.button === 2) {
                    tourne(element.querySelector("img"));
                    return;
                }
                else if (event.button === 0){
                    // Sinon, on commence à glisser l'élément
                    glisseSourisAppuie(event,element);
                }
            }
        }
            
            function flip(e) {
                var scaleX_valeur = window.getComputedStyle(e).transform;
                if (scaleX_valeur === 'none' || scaleX_valeur === 'matrix(1, 0, 0, 1, 0, 0)' || scaleX_valeur === 'matrix(0, -1, 1, 0, 0, 0)' || scaleX_valeur === 'matrix(0, 1, -1, 0, 0, 0)' || scaleX_valeur === 'matrix(-1, 0, 0, -1, 0, 0)') {
                    e.dataset.flip = "-1";
                    e.style.transform = `scaleX(-1)`;
                }
                else {
                    e.dataset.flip = "1";
                    e.style.transform = `scaleX(1)`;
                }
            }

            function tourne(e) {
                const transform = e.style.transform || '';
                const flip = transform.includes('scaleX(-1)');
                // Donne valeur numérique de la rotation
                rotation = e.style.transform.replace(/[^\d.]/g, '') || 0;
                if (flip) {
                    console.log(rotation)
                    if (rotation == 1){
                        rotation = 0
                    }
                    if (rotation == 10){
                        rotation = 0
                    }
                    if (rotation > 1){
                        rotation = rotation - 100
                    }
                    if (rotation > 181){
                        rotation = rotation - 900
                    }
                    console.log(rotation)
                    // Rotation de 90 degrés à partir de l'image actuelle
                    rotation = (parseInt(rotation) + 90) % 360;
                    e.dataset.rotation = `${rotation}`;
                    console.log(rotation)
                    e.style.transform = `scaleX(-1) rotate(${rotation}deg)`;
                }
                else {
                    console.log(rotation)
                    if (rotation == 1){
                        rotation = 0
                    }
                    // Rotation de 90 degrés à partir de l'image actuelle
                    rotation = (parseInt(rotation) + 90) % 360;
                    console.log(rotation)
                    e.dataset.rotation = `${rotation}`;
                    e.style.transform = `rotate(-${rotation}deg)`;
                }
            }

            function glisseSourisAppuie(e,element) {
                // Empêche le comportement par défaut du navigateur
                e.preventDefault();
                // Capturer la position de la souris au moment du clic
                pos3 = e.clientX;
                pos4 = e.clientY;
                // Attacher les événements pour déplacer l'élément
                document.onmouseup = function() { arreteGlisseElement(element); };
                document.onmousemove = function(event) { elementGlisse(event, element); };
            }

            function elementGlisse(e,element) {
                e.preventDefault();
                // Calculer la nouvelle position de l'élément
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;
                // Déplacer l'élément, element.offset... donne la position entre le parent et l'élément
                element.style.top = (element.offsetTop - pos2) + "px";
                element.style.left = (element.offsetLeft - pos1) + "px";
            }

            function arreteGlisseElement(element) {
                // Arrête le déplacement lorsque la souris est relâchée
                document.onmouseup = null;
                document.onmousemove = null;
                // Met à jour les coordonnées à la fin du déplacement
                updateCoords(element);
            }

            // Affiche les coordonnées actuelles
            function updateCoords(element) {
                // Récupère la position de l'élément
                var pos = element.getBoundingClientRect();
                // Pour le centre de l'image
                var centerX = Math.round(pos.left + pos.width / 2);
                var centerY = Math.round(pos.top + pos.height / 2);
                placementGrille(centerX,centerY,element)
            }
            
            function placementGrille(x,y,element) {
                var element = element.querySelector("img")
                // Le numéro de la case
                carreX = Math.round(((x-120)/760)*19);
                carreY = Math.round(((y-120)/760)*19);
                // Affiche le carré où va la pièce
                var carreText = "X: " + carreX + ", Y: " + carreY;
                document.getElementById("carre").textContent = carreText;
                elementReel = element.id;
                // Pour ne pas appeler valider le nombre de fois où l'on a cliqué sur le bouton Valider 
                console.log(envoie)
                if (envoie != null) {
                    document.getElementById("myButton").removeEventListener("click",envoie);
                }
                envoie =  function() {
                    valider(elementReel);
                }
                document.getElementById("myButton").addEventListener("click",envoie);
            }

            function valider(element) {
                const imgElement = document.getElementById(element);
                const retourne = parseInt(imgElement.dataset.flip) ||1;
                const rotation = parseInt(imgElement.dataset.rotation)||0;
                envoieValeur(carreX,carreY, retourne, -rotation , element);
            }
