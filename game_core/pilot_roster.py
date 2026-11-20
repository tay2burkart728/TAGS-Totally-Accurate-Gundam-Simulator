from game_core.gundams import Gundam

class Pilot:
    def __init__(self, name, gundam, portrait_name=None):
        """Pilot identities"""
        self.name = name
        self.gundam = gundam

        self.championships = 0
        self.semifinals = 0
        self.quarterfinals = 0
        self.wins = 0
        self.losses = 0
        self.eliminated = False

        if portrait_name is None:
            safe = name.lower().replace(" ", "_")
        else:
            safe = portrait_name.lower().replace(" ", "_")

        self.portrait_path = f"assets/portraits/{safe}.png"
        self.portrait_gray_path = f"assets/portraits/{safe}_gray.png"

    def __str__(self):
        """returns pilot and gundam pairings"""
        return f"{self.name} ({self.gundam.name})"

ROSTER = [
    Pilot("Amuro Ray",
          Gundam("RX-78-2", 5100, 640, 620, 270, 152, special="Newtype Awakened"),
          portrait_name="amuro"),
    Pilot("Banagher Links",
          Gundam("RX-0 Unicorn", 5700, 500, 1120, 330, 135, special="Beam Magnum"),
          portrait_name="banagher"),
    Pilot("Bellri Zenam",
          Gundam("YG-111 G-Self", 7200, 620, 560, 600, 95, special="Last Stand"),
          portrait_name="bellri"),
    Pilot("Char Aznable",
          Gundam("Zaku II", 4950, 600, 580, 240, 155, special="Red Comet"),
          portrait_name="char"),
    Pilot("Domon Kasshu",
          Gundam("Burning God", 5700, 1120, 480, 330, 135, special="Mutilation"),
          portrait_name="domon"),
    Pilot("Flit Asuno",
          Gundam("AGE-1", 6900, 600, 520, 590, 98, special="Retaliate"),
          portrait_name="flit"),
    Pilot("Garrod Ran",
          Gundam("GX-9901-DX", 8300, 540, 520, 580, 92, special="Missile Pod Ambush"),
          portrait_name="garrod"),
    Pilot("Gyunei Guss",
          Gundam("Jagd Doga", 5200, 480, 1000, 300, 130, special="Quad Funnels"),
          portrait_name="gyunei"),
    Pilot("Hathaway Noa",
          Gundam("RX-105 Xi", 5400, 450, 1080, 320, 128, special="ECM"),
          portrait_name="hathaway"),
    Pilot("Heero Yuy",
          Gundam("XXXG-01W", 4700, 650, 600, 260, 148, special="Twin Buster Rifles"),
          portrait_name="heero"),
    Pilot("Judau Ashta",
          Gundam("Double Zeta", 5200, 1000, 500, 300, 128, special="Follow-Up Strike"),
          portrait_name="judau"),
    Pilot("Kamille Bidan",
          Gundam("MSZ-006 Zeta", 8500, 560, 560, 540, 95, special="Berserker"),
          portrait_name="kamille"),
    Pilot("Kira Yamato",
          Gundam("Mighty Strike Freedom", 8700, 600, 580, 520, 98, special="Full-Burst Dragoon"),
          portrait_name="kira"),
    Pilot("Mikazuki Augus",  
          Gundam("Barbatos", 5600, 1100, 450, 320, 130, special="Mace"),
          portrait_name="mikazuki"),
    Pilot("Seabook Arno",
          Gundam("F91", 5000, 520, 980, 275, 132, special="Beam Shield"),
          portrait_name="seabook"),
    Pilot("Setsuna F. Seiei",
          Gundam("GN-001", 4550, 620, 560, 235, 150, special="Afterimage Stun"),
          portrait_name="setsuna"),
    Pilot("Suletta Mercury",
          Gundam("XVX-016", 7000, 580, 580, 620, 92, special="Permet Overheat"),
          portrait_name="suletta"),
    Pilot("Uso Ewin",
          Gundam("Victory", 5000, 980, 520, 275, 132, special="Field Repair"),
          portrait_name="uso"),
]
