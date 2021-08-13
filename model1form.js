var cars={
    'Toyota':['Yaris','Vios','Wish','Innova','Sienta','Sienna','RAV4','Prius c','Prius PHV','Prius Alpha','Prius','Previa','Land Cruiser','Altis','Camry','C-HR','Alphard','86'],
    'Ford':['Focus','Focus Active','Focus Wagon','Kuga','Mustang','Ranger','Tourneo Custom','Mondeo','Mondeo Wagon','Escort','Fiesta','EcoSport'],
    'Nissan':['370Z','Altima','GT-R','Juke','Kicks','Leaf','Sentra','Tiida','X-Trail','Teana','Livina','March','Murano','Rogue'],
    'Mercedes-Benz':['A-Class','A-Class Sedan','AMG GT','AMG GT 4-Door Coupe','B-Class','C-Class Cabriolet','C-Class Coupe','C-Class Estate','C-Class Sedan','CLA','CLA Shooting Brake','CLS','E-Class Coupe','E-Class Estate','E-Class Sedan','EQC','G-Class','GLA','GLB','GLC','GLC Coupe','GLE','GLE Coupe','GLS','S-Class','V-Class','Vito Tourer'],
    'BMW':['1-Series','2-Series Active Tourer','2-Series Gran Coupe','2-Series Gran Tourer','3-Series Sedan','3-Series Touring','4-Series','4-Series Convertible','5-Series Sedan','5-Series Touring','6-Series Gran Turismo','7-Series','8-Series','8-Series Gran Coupe','X1','X2','X3','X4','X5','X6','X7','Z4'],
    'Mitsubishi':['Delica','Zinger','Fortis','Veryca','Colt Plus','Outlander','Lancer Io','Savrin','Lancer Fortis','Canter','Grunder','Eclipse','Lancer','Grand Lancer','Leadca','Varica','Freeca','Lancer Sportback','Global Lancer','Virage Io','Space Gear','Veryca Magic','Galant','Super Delica','New Canter','Evo','Pajero','Asx'],
    'Suzuki':['Carry','Sx4','Swift','Vitara','Jimny','Ignis','Grand Vitara','Solio','Swift ','Vitara ','Baleno','Super Carry','Alto','G.Vitara','Every','Escudo','Liana'],
    'Honda':['Cr-V', 'Hr-V', 'Fit', 'City', 'Civic', 'Accord', 'Odyssey','Civic ', 'Odyssey ', 'City ', 'Accord ','Cr-Z', 'Ferio', 'Insight Hybrid', 'K6', 'Type R',],
    'Mazda':['Mazda 5', 'Mazda 3', 'Cx-3', 'Cx-5', 'Cx-9', 'Mazda6', 'Tribute', 'Mpv', 'Premacy','Mx-5', 'Cx-7', 'Rx-8', 'Protege','Mazda 2','Bongo','Isamu','Capella','E2000','Rx-7',],
    'Hyundai':['Santa Fe','Tucson','Ix35','Elantra','Kona','Starex','I30','Porter','Matrix','I10','Verna','Getz','Veloster','Grand Starex','Sonata','Veloster '],
    'Luxgen':['U6','M7','U7','S5','S3','Urx'],
    'Subaru':['Forester','Levorg','Outback','Xv','Wrx','Legacy','Impreza','Brz'],
    'Lexus':['Is200T','Rx200T','Nx200T','Nx200','Rx300','Ux200','Es250','Is250','Es240','Rx400H','Ct200H','Es300H','Rx450H','Is300H','Gs250','Rx270','Rx350','Ls460L','Nx300H','Rx330','Es200','Nx300','Es350','Gs300','Lx470','Gs300H','Is200','Is 300','Es330'],
    'Kia':['Morning','Kaon','Picanto','Carens','Soul','Sportage'],
    'Vw':['Scirocco','Tiguan','Golf','T6','T4','Touran','Passat','T5','Polo','T-Cross','Caddy','Phaeton','Amarok','Crafter','Vento','Sharan','Touareg','Beetle','Jetta','Lupo','Pointer'],
    'Landrover':['Discovery','Evoque','Freelander','Defender'],
    'Skoda':['Kodiaq','Octavia','Citigo','Yeti','Fabia','Rapid','Karoq','Roomster','Superb','Scala','Kamiq'],
    'Mini':['Copper','Countryman','Cabrio S','Clubman','Mini Jcw','Paceman','Hatch',],
    'Volvo':['Xc60','V60','V40','S40','V50','Xc90','S60','S80','S90','Xc90 ','Xc70','C30','740','V90','940','Xc40','S70',],
    'Audi':['A1','S5','A3','A6','A4','Tt','A7','A5','Q7','Q3','S4','R8','Rs6','Q2','Q5','S3','A8'],
    'Smart':['Forfour','Fortwo','Roadster'],
    'Peugeot':['3008','2008','208','508','206','107','308','207','1007','5008','Traveller','406','106','407','307','Rifter'],
    'Porsche':['Macan','Cayenne','Boxster','Cayman','Panamera','Carrera','Taycan',],
    'Citroen':['C4','C2','Saxo','C3'],
    'Infiniti':['Q30','Q50','Qx70','Fx35','G37','G35','Jx','Fx37','Q70','Qx60','Ex35','M37','Qx30','G25','Fx','Qx50','M35','Jx35','Qx4',],
    'Jaguar':['X-Type','F-Pace','Xe','Xk','Xf','Xj6','Xfr','S-Type','I-Pace','Xjs','Xj','F-Type','Xkr','Xjl','E-Pace','F-Type Coupe','Vanden Plas','Xj8'],
    'Isuzu':['Elf','Rodeo','Nlr','Nkr','Trooper'],
    'Lamborghini':['Gallardo','Lp560-4','Lp570-4'],
    'Ferrari':['Spider','Italia'],
    'Alfa Romeo':['Giulia','Stelvio','Giulietta'],
    'Chevrolet':['Camaro','Corvette','Zl1'],
    'Dodge':['Challenger','Ram','Charger'],
    'Maserati':['Granturismo','Levante','Ghibli','Quattroporte'],
    'Opel':['Zafira','Astra','Corsa','Speedster'],
    'Saab':['Sedan','Convertible'],
    'Fiat':['Panda','Abarth'],
    'Jeep':['Cherokee','Wrangler'],
    'Bentley':['Continental','Flying Spur'],
    'Mclaren':['Mp4','650S'],
    'Chrysler':['300C','Town Country'],
    'Tesla':['Model X','Model 3','Model S'],
    'Buick':['Lucerne Cxl','Lacrosse','Rendezvous','Excelle'],
    'Cmc':['Veryca','Zinger','Magic','Leadca'],
    'Renault':['Clio','Megane Cabriolet'],
    'Hummer':['H2','H3'],
    'Scion':['Corolla Altis'],
    'Rolls-Royce':['Silver'],
    'Acura':['Cl','Coupe','Mdx'],
    'Cadillac':['Sts','Allante','Srx','Dts','Cts'],
    'Iveco':['Daily'],
    'Formosa':['Matiz'],
    'Aston Martin':['Vantage','Rapide'],
}

var carBrand = document.getElementById('car_brand_id');
var carModel = document.getElementById('car_model_id');
console.log(10)

carBrand.addEventListener('change', function(){

var selected_option = cars[this.value];
console.log(this.value)

while(carModel.options.length >0 ){
    carModel.options.remove(0);
}

Array.from(selected_option).forEach(function(el){
    let option = new Option(el,el);
    carModel.appendChild(option);
    console.log(carModel.appendChild(option))
})

})



