import numpy as np


def build_att(A, R):
    att_list = {a: [] for a in A}
    for att, target in R:
        if target in att_list:
            att_list[target].append(att)
        else:
            att_list[target] = [att]
    return att_list


def h_categorizer(A, R, w, max_iter, epsi=1e-4):

    # on construit dans un premier temps le dictionnaire des attaques
    # on ajoute pour chaque argument a une liste des arguments qui l'attaquent
    attaquand = build_att(A, R)

    # on initialise les poids courants avec les poids initiaux
    hc = {a: w[a] for a in A}

    for iteration in range(max_iter):
        # On crée un nouveau dictionnaire pour stocker les valeurs calculées à cette itération
        new_hc = {}

        for a in A:
            liste_attaquants = attaquand[a]
            # On calcule la somme des valeurs hc actuelles de tous ces attaquants
            somme_attaquants = 0
            for b in liste_attaquants:
                somme_attaquants += hc[b]

            # update de la valeur de 'a' avec la formule : HC_{k+1}(a) = w(a) / (1 + somme des attaquants) puis on save
            newVal = w[a] / (1 + somme_attaquants)
            new_hc[a] = newVal

        # On vérifie la convergence en comparant les nouvelles valeurs avec les anciennes
        diff = max(abs(new_hc[a] - hc[a]) for a in A)
        hc = new_hc

        if diff < epsi:
            break

    return hc


def dict_to_vector(A, d):
    return np.array([d[a] for a in A], dtype=float)


def sample_and_compute_X(A, R, epsilon=1e-4, max_iter=1000, n_samples=10000, seed=42, controlled_args=None):

    # générateur de nombres aléatoires pour les vecteurs
    rng = np.random.default_rng(seed)

    # on initialise la matrice des résultats
    X = np.zeros((n_samples, len(A)), dtype=float)

    for i in range(n_samples):

        # 1. Génère un vecteur aléatoire de poids w
        w_rng_values = rng.random(len(A))
        w = dict(zip(A, w_rng_values))

        if controlled_args:
            for arg, value in controlled_args.items():
                w[arg] = value

        # 2. Calcule le vecteur x correspondant
        HC = h_categorizer(A, R, w, max_iter, epsilon)

        # 3. Enregistre ce vecteur dans la matrice X
        X[i, :] = dict_to_vector(A, HC)

    return X
