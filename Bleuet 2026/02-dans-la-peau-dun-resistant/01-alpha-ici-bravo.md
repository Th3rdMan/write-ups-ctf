# Alpha ici Bravo

![1. Alpha ici Bravo](./assets/1-alpha-ici-bravo.png)

> Votre grand-père adorait se mettre dans la peau de résistants. Il est parvenu à obtenir l'[archive audio](https://bleuet.aege.fr/files/f0a4740d14f2b11c4914dd46b14b2025/CTF_Bleuet_2K26_-_Alpha_ici_Bravo_-_audio.wav) d'un enregistrement radio intercepté en 1944. Il avait noté que cet enregistrement semblait provenir d’un maquis de la résistance capté accidentellement lors d’une transmission clandestine. Un largage de matériel y était programmé dans les jours suivants la transmission, mais le lieu exact de réception était inconnu.

Votre grand-père s'était donné pour mission de localiser la commune concernée par ce largage à partir des seuls éléments donnés.

**Format du flag** : `Nomcommune`

[Audio fourni](./assets/1-audio.wav)

---

Première étape : isoler les voix du bruit de la locomotive. [Lalal.ai](https://www.lalal.ai/) permet d’obtenir une voix plus exploitable. Le résultat reste imparfait, mais il permet d’identifier plusieurs noms de gares.

Le train part de **Veynes** en direction de **Briançon**. Depuis la gare d’où le message semble être diffusé, la ligne dessert notamment **Embrun**, **L’Argentière-la-Bessée** et **Prelles**. Cette dernière est fermée depuis 1960, ce qui reste cohérent avec le contexte historique.

**Source :** [Ligne Veynes-Briançon](https://routes.fandom.com/wiki/Ligne_Veynes_-_Brian%C3%A7on#Haltes)

![1. Veynes-Briançon](./assets/1-veynes-briancon.png)

Un plan d’époque de la ligne entre Veynes et Embrun permet ensuite de réduire le champ des communes possibles. L’enregistrement semble avoir lieu dans une gare de ce tronçon.

**Source :** [Train Consultant — La Transalpine Livron-Mont-Cenis](https://trainconsultant.com/2024/08/29/la-transalpine-livron-mont-cenis/)

![1. Ligne Veynes-Embrun](./assets/1-ligne-veynes-embrun.png)

À ce stade, tout semble pointer vers le **cirque de Morgon**. Le site est lié à des parachutages et l’un de ses panoramas rappelle une image marquante du CTF Bleuet de France précédent.

<img src="./assets/1-grand-morgon.png" alt="1. Grand Morgon" width="221">

*Grand Morgon, un des lieux de parachutage, non loin de Savines-le-Lac.*

Première hypothèse : **Crots**, commune à laquelle est rattaché le Grand Morgon. La réponse est refusée.

⛔ **Fail :** `Crots`

Les tentatives suivantes se concentrent sur les gares et les communes proches de cette hypothèse. Aucun flag ne passe.

⛔ **Fail :** `Savines`  
⛔ **Fail :** `Savineslelac`  
⛔ **Fail :** `Prunieres`

La reprise du raisonnement fait ressortir plusieurs mentions de Morgon parmi les lieux de parachutage, ainsi que du maquis de **Chorges**. Chorges est aussi le lieu suivant sur le plan ferroviaire. La piste est plus solide que les premiers guesses.

✅ **Réponse :** `Chorges`
