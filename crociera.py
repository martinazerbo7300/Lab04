class Crociera:
    def __init__(self, nome):
        self.nome = nome
        self.cabine = []
        self.passeggeri = []


    def get_nome(self):
        return self.nome
    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome

    def carica_file_dati(self, file_path):
        import os
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} non trovato.")

        with open(file_path, "r") as f:
            for riga in f:
                campi = riga.strip().split(",")
                if not campi:
                    continue

                # Cabina
                if campi[0].startswith("CAB"):
                    codice, letti, ponte, prezzo_base = campi[0], int(campi[1]), int(campi[2]), float(campi[3])
                    if len(campi) == 4:
                        cabina = {
                            "tipo": "Standard",
                            "codice": codice,
                            "letti": letti,
                            "ponte": ponte,
                            "prezzo_base": prezzo_base,
                            "disponibile": True
                        }
                    elif len(campi) == 5:
                        extra = campi[4]
                        if extra.isdigit():
                            cabina = {
                                "tipo": "Animali",
                                "codice": codice,
                                "letti": letti,
                                "ponte": ponte,
                                "prezzo_base": prezzo_base,
                                "max_animali": int(extra),
                                "disponibile": True
                            }
                        else:
                            cabina = {
                                "tipo": "Deluxe",
                                "codice": codice,
                                "letti": letti,
                                "ponte": ponte,
                                "prezzo_base": prezzo_base,
                                "stile": extra,
                                "disponibile": True
                            }
                    self.cabine.append(cabina)

                # Passeggero
                elif campi[0].startswith("P"):
                    passeggero = {
                        "codice": campi[0],
                        "nome": campi[1],
                        "cognome": campi[2],
                        "cabina": None
                    }
                    self.passeggeri.append(passeggero)


    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        cabina = next((c for c in self.cabine if c["codice"] == codice_cabina), None)
        if cabina is None:
            raise ValueError(f"Cabina {codice_cabina} inesistente.")
        if not cabina["disponibile"]:
            raise ValueError(f"Cabina {codice_cabina} non disponibile.")

        passeggero = next((p for p in self.passeggeri if p["codice"] == codice_passeggero), None)
        if passeggero is None:
            raise ValueError(f"Passeggero {codice_passeggero} inesistente.")
        if passeggero["cabina"] is not None:
            raise ValueError(f"Passeggero {codice_passeggero} già assegnato alla cabina {passeggero['cabina']}.")

        cabina["disponibile"] = False
        passeggero["cabina"] = cabina["codice"]


    def cabine_ordinate_per_prezzo(self):
        def prezzo_finale(c):
            if c["tipo"] == "Standard":
                return c["prezzo_base"]
            elif c["tipo"] == "Animali":
                return c["prezzo_base"] * (1 + 0.10 * c["max_animali"])
            elif c["tipo"] == "Deluxe":
                return c["prezzo_base"] * 1.20
        return sorted(self.cabine, key=prezzo_finale)



    def elenca_passeggeri(self):
        for p in self.passeggeri:
            cabina_info = p["cabina"] if p["cabina"] else "Nessuna cabina"
            print(f"{p['codice']}: {p['nome']} {p['cognome']} - Cabina: {cabina_info}")
