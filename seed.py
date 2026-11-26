"""Create db/catbuild.db from schema.sql and export public/data.json (static fallback)."""
import sqlite3, json, os
os.makedirs("db", exist_ok=True)
con = sqlite3.connect("db/catbuild.db")
con.executescript("DROP TABLE IF EXISTS gallery; DROP TABLE IF EXISTS packages; DROP TABLE IF EXISTS specs;")
con.executescript(open("schema.sql").read())

G = {
 "plans": [("006","2D Floor Plan"),("093","2-Storey Residential Concept Sheet"),("094","3D Elevation Study"),("095","Perspective View"),("159","Top View – Layout 1"),("160","Top View – Layout 2"),("191","Furnished Plan Render")],
 "stages": [("096","Site Cleaning"),("097","Bore Well"),("101","Site Marking"),("099","Column Footing"),("100","Column Footing Concrete"),("102","Plinth Beam Shuttering"),("103","Plinth Beam Concrete"),("104","Plinth to Floor Wall Work"),("105","Earth Filling"),("106","PCC Work for Flooring"),("107","RCC Work for Flooring"),("108","Curing Work"),("109","Column Work"),("110","Column Shuttering"),("111","Brick Work to Sill Level"),("112","Brick Work to Lintel Level"),("113","Roof Slab Reinforcement"),("114","Roof Concrete"),("115","Elevation Work"),("116","Plastering Work"),("117","Paint & Finishing"),("118","Side View"),("119","Front View")],
 "finishes": [("120","Door (Teak Wood)"),("121","Window"),("122","Door (Flush)"),("123","Bathroom Fittings"),("124","Bathroom Fittings"),("125","Bathroom Fittings"),("126","Shelf – Cuddapah Stone"),("127","Wall Finishes (Paint)"),("128","Kitchen Countertop – Cuddapah Stone")],
 "elevations": [(i,"3D Elevation") for i in "135 136 137 138 139 140 141 142 143 144 145 146 149 150 151 152 154 155 156 185 187 189 190 192".split()],
 "interiors": [(i,"Interior Design") for i in "157 158 161 163 164 165 166 167 168 169 173 175 177 181".split()],
 "completed": [("286","Completed Home"),("287","Completed Pavilion"),("316","Completed Project"),("317","Completed Project"),("318","Completed Project"),("292","Interior – Partition"),("293","Interior – Ceiling"),("297","Interior – Wall Panel"),("301","Interior – TV Unit"),("303","Interior – Foyer"),("305","Interior – Wardrobe"),("306","Interior – Kitchen"),("308","Interior – Hall")],
 "pooja": [(i,"Bhoomi Pooja 2024–25") for i in "236 237 239 240 241 243 247 250 251 253 254".split()],
}
for cat, rows in G.items():
    for n,(img,t) in enumerate(rows):
        con.execute("INSERT INTO gallery(category,title,image,sort_order) VALUES(?,?,?,?)",(cat,t,f"img/{img}.jpg",n))

P = [
 ("Economic",2100,"196",["Cement – Dalmia","Steel – Kamatchi, Pulkit 550D","Bricks – Kalavasal brick","Sand – M-sand, P-sand","Main frame & door – imported","Inner frames – imported, Vembu wood","Windows – UPVC sliding","Floor tiles 2x2 vitrified up to ₹30","Wall tiles ceramic up to ₹30","Wires – Kundan; Switches – Roma"]),
 ("Smart",2290,"197",["Cement – Dalmia","Steel – Amman, Kamatchi, Pulkit 550D","Bricks – Chamber","Main frame & door – Teak","Inner frames – Mahogany, Kumil wood","Windows – UPVC sliding or Mahogany","Floor tiles 2x2 vitrified up to ₹40","Wall tiles ceramic up to ₹45","Wires – Finolex or Kundan","Painting – whitewash inside & outside"]),
 ("Prime",2490,"198",["Cement – UltraTech","Steel – JSW, Agni, ISteel 550D","Bricks – Wire-cut","Main frame & door – Teak","Inner frames – Vengai, Padauk","Floor tiles 2x2, 4x2 up to ₹60","Switches – Hifi; Plumbing – Parryware","Paint – putty, primer & colour (JSW)","Septic tank & sump","Interior free: semi kitchen, wardrobe, TV unit"]),
 ("Prime+",2690,"199",["Cement – UltraTech or Ramco","Steel – TATA 550SD","Bricks – Chamber","Main frame & inner frames – Kerala Teak","Floor tiles 2x2, 4x2 up to ₹75","Switches – Legrand or GM; Plumbing – Jaguar","Paint – Asian brand","Interior free: full kitchen, wardrobe, TV unit, false ceiling","Septic tank & sump; compound wall (above 2000 sq.ft)","CCTV camera & smart switches"]),
]
for n,r,i,items in P:
    con.execute("INSERT INTO packages(name,rate_per_sqft,image,items) VALUES(?,?,?,?)",(n,r,f"img/{i}.jpg",json.dumps(items,ensure_ascii=False)))

S = {
 "Basement Works": ["Earth excavation up to hard soil (7 ft)","Sand filling 12\" thick","PCC (1:5:10) 12\" for footing; RCC (1:1.5:3) 1'6\" footing","Plinth beam 1'6\" x 9\" with 16mm, 12mm rod & 8mm ring","Basement height 4 ft (as per structural drawing)"],
 "Walls & Accessories": ["Main wall brick work 9\"; partition wall 4.5\"","Polished Cuddapah slab 4' x 7' for kitchen and bedrooms","Bathroom ventilation 3' x 2'; kitchen exhaust fan provision 9\"","Lintel and sunshade wherever necessary"],
 "Roof & Steps": ["Roof height 10 ft from floor level","Roof slab 5\" with 12mm, 10mm & 8mm rod","Parapet wall 6\" thick, 3 ft high","Staircase with stainless steel rails"],
 "Tile Works": ["Vitrified floor tiles ₹50 (±5)","Kitchen & toilet wall tiles ₹35 (±5)","Anti-skid bathroom tiles ₹35 (±5)","Bathroom wall tiles 7 ft high; granite kitchen top; stainless steel sink"],
 "Doors & Windows": ["Main door frame – Teak; ready-made Teak door 5' x 7'","Bedroom doors – FRB 3' x 7'; bathroom doors – PVC 2'6\" x 7'","Windows – UPVC with mosquito net or wooden frame"],
 "Plumbing & Electrical": ["Kitchen tap point 1, bathroom tap points 2","Fan point with regulator and 2 light points per room","Plug points, TV socket, water purifier & heater points","Solar water heater connection provision"],
 "Painting Works": ["Inner walls – 2 coat putty, 1 primer, 2 colour","Ceiling – 2 putty, 1 primer, 1 white","Outer walls – 1 whitewash, 2 emulsion","Main door polish"],
 "Excluded (Special Charges)": ["Plan approval, land & house tax","Water supply & EB charges until completion","Modular kitchen, interiors, other wooden works","Bore well, sump motor, grill gates, compound & outer works","Free: AutoCAD 2D plan & 3D elevation drawing"],
}
for k,v in S.items():
    con.execute("INSERT INTO specs(section,items) VALUES(?,?)",(k,json.dumps(v,ensure_ascii=False)))
con.commit()

def rows(q): 
    cur=con.execute(q); cols=[c[0] for c in cur.description]; return [dict(zip(cols,r)) for r in cur]
out={"gallery":rows("SELECT category,title,image FROM gallery ORDER BY category,sort_order"),
     "packages":[{**p,"items":json.loads(p["items"])} for p in rows("SELECT name,rate_per_sqft,image,items FROM packages")],
     "specs":[{**s,"items":json.loads(s["items"])} for s in rows("SELECT section,items FROM specs")]}
json.dump(out,open("public/data.json","w"),ensure_ascii=False)
print("seeded:",len(out["gallery"]),"gallery,",len(out["packages"]),"packages")
