import random
from player import Player  


class Roulette:
    def __init__(self, player):
        self.roulette_wheel = {
            0: 'groen',
            1: 'rood', 2: 'zwart', 3: 'rood', 4: 'zwart', 5: 'rood', 6: 'zwart',
            7: 'rood', 8: 'zwart', 9: 'rood', 10: 'zwart', 11: 'zwart', 12: 'rood',
            13: 'zwart', 14: 'rood', 15: 'zwart', 16: 'rood', 17: 'zwart', 18: 'rood',
            19: 'rood', 20: 'zwart', 21: 'rood', 22: 'zwart', 23: 'rood', 24: 'zwart',
            25: 'rood', 26: 'zwart', 27: 'rood', 28: 'zwart', 29: 'zwart', 30: 'rood',
            31: 'zwart', 32: 'rood', 33: 'zwart', 34: 'rood', 35: 'zwart', 36: 'rood'
        }
        self.player = player
        self.ball = None

    def spin_wheel(self):
        nummer = random.randint(0, 36)
        kleur = self.roulette_wheel[nummer]
        self.ball = (nummer, kleur)
        print(f"🎡 De bal is geland op {nummer} ({kleur})")
        return nummer, kleur

    def place_bet(self):
        print(f"\n💰 Jouw saldo: €{self.player.cash}")
        try:
            bedrag = int(input("Hoeveel wil je inzetten? €"))
            if bedrag <= 0 or bedrag > self.player.cash:
                print("❌ Ongeldige inzet.")
                return

            print("Je kunt inzetten op: kleur (rood/zwart/groen), nummer (0-36), of even/oneven")
            bet_type = input("Waar wil je op inzetten? ('kleur', 'nummer', 'even/oneven'): ").strip().lower()

            if bet_type == "kleur":
                keuze = input("Kies kleur (rood/zwart/groen): ").strip().lower()
                if keuze not in ['rood', 'zwart', 'groen']:
                    print("❌ Ongeldige kleur.")
                    return

                nummer, kleur = self.spin_wheel()
                if keuze == kleur:
                    self.player.cash += bedrag
                    print(f"✅ Je wint! Nieuwe saldo: €{self.player.cash}")
                else:
                    self.player.cash -= bedrag
                    print(f"❌ Verloren. Nieuwe saldo: €{self.player.cash}")

            elif bet_type == "nummer":
                try:
                    keuze = int(input("Kies een nummer (0-36): "))
                    if keuze < 0 or keuze > 36:
                        print("❌ Ongeldig nummer.")
                        return

                    nummer, kleur = self.spin_wheel()
                    if keuze == nummer:
                        winst = bedrag * 35
                        self.player.cash += winst
                        print(f"🎉 Je wint €{winst}! Nieuwe saldo: €{self.player.cash}")
                    else:
                        self.player.cash -= bedrag
                        print(f"❌ Verloren. Nieuwe saldo: €{self.player.cash}")
                except ValueError:
                    print("❌ Ongeldig nummer.")

            elif bet_type == "even/oneven":
                keuze = input("Kies 'even' of 'oneven': ").strip().lower()
                if keuze not in ['even', 'oneven']:
                    print("❌ Ongeldige keuze.")
                    return

                nummer, kleur = self.spin_wheel()
                if nummer == 0:
                    print("0 is geen even of oneven. Automatisch verloren.")
                    self.player.cash -= bedrag
                    print(f"❌ Verloren. Nieuwe saldo: €{self.player.cash}")
                    return

                if (nummer % 2 == 0 and keuze == 'even') or (nummer % 2 != 0 and keuze == 'oneven'):
                    self.player.cash += bedrag
                    print(f"✅ Je wint! Nieuwe saldo: €{self.player.cash}")
                else:
                    self.player.cash -= bedrag
                    print(f"❌ Verloren. Nieuwe saldo: €{self.player.cash}")
            else:
                print("❌ Ongeldige inzet-optie.")
        except ValueError:
            print("❌ Ongeldige invoer.")

    def start_game(self):
        print("🎰 Welkom bij Roulette!")
        while self.player.cash > 0:
            self.place_bet()
            verder = input("Wil je doorgaan? (j/n): ").strip().lower()
            if verder != 'j':
                break
        print(f"👋 Spel afgelopen. Eindsaldo: €{self.player.cash}")

