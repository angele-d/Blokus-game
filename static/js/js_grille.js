        window.onload = () => genere_grille(id_game);
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
        function updategrille(){
            genere_grille(id_game)
        }
       
        let isUpdating = false;
        setInterval(() => {
            if (!isUpdating) {
                isUpdating = true;
                genere_grille(id_game).finally(() => {
                    isUpdating = false;
                });
            }
        }, 2000);
        
        
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
                    nonid.remove();
                console.log('Réponse du serveur:', result);}

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
            element.addEventListener('dblclick',function (){
                flip(element.querySelector("img"))
                doubleClic = true;
            })
            element.querySelector("img").onmousedown = function(event){
                event.preventDefault();
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
                // Donne valeur numérique de la rotation
                rotation = e.style.transform.replace(/[^\d.]/g, '') || 0;
                // Rotation de 90 degrés à partir de l'image actuelle
                rotation = (parseInt(rotation) + 90) % 360;
                e.dataset.rotation = `${rotation}`;
                e.style.transform = `rotate(-${rotation}deg)`;
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
                var coordsText = "X: " + centerX + ", Y: " + centerY;
                // Met à jour
                document.getElementById("coords").textContent = coordsText;
            }
            
            function placementGrille(x,y,element) {
                var element = element.querySelector("img")
                // Le numéro de la case
                carreX = Math.round(((x-120)/760)*20);
                carreY = Math.round(((y-120)/760)*20);
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
