# 'categories': Add on to the end value is the dollar value given back
# 'dining': 5812, 5814
# 'entertainment', 
# 'gas': 4900, 5541, 5172, 9752 
# 'grocery': 5411, 9751, 5300, 5715
# 'hotel', 
# 'onlineDining', 
# 'onlineGrocery', 
 
# 'rentalCar', 
# 'retail', 
# 'streaming', 
# 'transit', 
# 'travel'

# 'other'

hotel_mcc_codes = [
    3501, 3502, 3503, 3504, 3505, 3506, 3507, 3508, 3509, 3510, 3511,
    3512, 3513, 3514, 3515, 3516, 3517, 3518, 3519, 3520, 3521, 3522,
    3523, 3524, 3525, 3526, 3527, 3528, 3529, 3530, 3531, 3532, 3533,
    3534, 3535, 3536, 3537, 3538, 3539, 3540, 3541, 3542, 3543, 3544,
    3545, 3546, 3547, 3548, 3549, 3550, 3551, 3552, 3553, 3554, 3555,
    3556, 3557, 3558, 3559, 3560, 3561, 3562, 3563, 3564, 3565, 3566,
    3567, 3568, 3569, 3570, 3571, 3572, 3573, 3574, 3575, 3576, 3577,
    3578, 3579, 3580, 3581, 3582, 3583, 3584, 3585, 3586, 3587, 3588,
    3589, 3590, 3591, 3592, 3593, 3594, 3595, 3596, 3597, 3598, 3599,
    3600, 3601, 3602, 3603, 3604, 3605, 3606, 3607, 3608, 3609, 3610,
    3611, 3612, 3613, 3614, 3615, 3616, 3617, 3618, 3619, 3620, 3621,
    3622, 3623, 3624, 3625, 3626, 3627, 3628, 3629, 3630, 3631, 3632,
    3633, 3634, 3635, 3636, 3637, 3638, 3639, 3640, 3641, 3642, 3643,
    3644, 3645, 3646, 3647, 3648, 3649, 3650, 3651, 3652, 3653, 3654,
    3655, 3656, 3657, 3658, 3659, 3660, 3661, 3662, 3663, 3664, 3665,
    3666, 3667, 3668, 3669, 3670, 3671, 3672, 3673, 3674, 3675, 3676,
    3677, 3678, 3679, 3680, 3681, 3682, 3683, 3684, 3685, 3686, 3687,
    3688, 3689, 3690, 3691, 3692, 3693, 3694, 3695, 3696, 3697, 3698,
    3699, 3700, 3701, 3702, 3703, 3704, 3705, 3706, 3707, 3708, 3709,
    3710, 3711, 3712, 3713, 3714, 3715, 3716, 3717, 3718, 3719, 3720,
    3721, 3722, 3723, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3731,
    3732, 3733, 3734, 3735, 3736, 3737, 3738, 3739, 3740, 3741, 3742,
    3743, 3744, 3745, 3746, 3747, 3748, 3749, 3750, 3751, 3752, 3753,
    3754, 3755, 3756, 3757, 3758, 3759, 3760, 3761, 3762, 3763, 3764,
    3765, 3766, 3767, 3768, 3769, 3770, 3771, 3772, 3773, 3774, 3775,
    3776, 3777, 3778, 3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786,
    3787, 3788, 3789, 3790, 3791, 3792, 3793, 3794, 3795, 3796, 3797,
    3798, 3799, 3800, 3801, 3802, 3803, 3804, 3805, 3806, 3807, 3808,
    3809, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3819,
    3820, 3821, 3822, 3823, 3824, 3825, 3826, 3827, 3828, 3829, 3830,
    7011  
]

entertainment_mcc_codes = [
    7832,  # Motion Picture Theaters
    7922,  # Theatrical Producers (except Motion Pictures), Ticket Agencies
    7929,  # Bands, Orchestras, and Miscellaneous Entertainers
    7933,  # Bowling Alleys
    7941,  # Commercial Sports, Professional Sports Clubs, Athletic Fields
    7991,  # Tourist Attractions and Exhibits
    7992,  # Public Golf Courses
    7996,  # Amusement Parks, Carnivals, Circuses, Fortune Tellers
    7997,  # Membership Clubs (Sports, Recreation, Athletic), Country Clubs
    7998,  # Aquariums, Dolphinariums, Zoos, and Seaquariums
    7999,  # Recreation Services (e.g., amusement parks, sports complexes)
    7800,  # Amusement and Recreation Services – Miscellaneous
    7841   # Video Tape Rental Stores
]

rental_car_mcc_codes = [
    3351,  # Car Rental Companies (e.g., Hertz)
    3352,  # Car Rental Companies (e.g., Avis)
    3353,  # Car Rental Companies (e.g., National)
    3354,  # Car Rental Companies (e.g., Budget)
    3355,  # Car Rental Companies (e.g., Enterprise)
    3356,  # Car Rental Companies (e.g., Thrifty)
    3357,  # Car Rental Companies (e.g., Dollar)
    3358,  # Car Rental Companies (e.g., Alamo)
    3359,  # Car Rental Companies (e.g., other unspecified)
    3360,  # Truck and Utility Trailer Rental
    7512   # Automobile Rental Agency
]

retail_mcc_codes = [
    5310,  # Discount Stores
    5311,  # Department Stores
    5331,  # Variety Stores
    5399,  # Miscellaneous General Merchandise Stores
    5611,  # Men's and Boys' Clothing and Accessories Stores
    5621,  # Women's Ready-to-Wear Stores
    5631,  # Women's Accessory and Specialty Stores
    5641,  # Children's and Infants' Wear Stores
    5651,  # Family Clothing Stores
    5655,  # Sports Apparel, Riding Apparel Stores
    5661,  # Shoe Stores
    5681,  # Furriers and Fur Shops
    5691,  # Men's and Women's Clothing Stores
    5697,  # Tailors, Seamstresses, Mending, and Alterations
    5698,  # Wig and Toupee Stores
    5699,  # Miscellaneous Apparel and Accessory Shops
    5712,  # Furniture, Home Furnishings Stores, Equipment Stores
    5713,  # Floor Covering Stores
    5714,  # Drapery, Window Covering, and Upholstery Stores
    5718,  # Fireplace, Fireplace Screens, and Accessories Stores
    5719,  # Miscellaneous Home Furnishing Specialty Stores
    5722,  # Household Appliance Stores
    5732,  # Electronics Stores
    5733,  # Music Stores, Musical Instruments, Pianos, Sheet Music
    5734,  # Computer Software Stores
    5735,  # Record Stores
    5815,  # Digital Goods: Media, Books, Movies, Music
    5912,  # Drug Stores and Pharmacies
    5940,  # Bicycle Shops
    5941,  # Sporting Goods Stores
    5942,  # Book Stores
    5943,  # Stationery Stores, Office, and School Supply Stores
    5944,  # Jewelry Stores
    5945,  # Hobby, Toy, and Game Shops
    5946,  # Camera and Photographic Supply Stores
    5947,  # Gift, Card, Novelty, and Souvenir Shops
    5948,  # Luggage and Leather Goods Stores
    5949,  # Fabric, Needlework, Piece Goods Stores
    5950,  # Glassware and Crystal Stores
    5964,  # Catalog Merchant
    5965,  # Direct Marketing – Catalog Merchants
    5969,  # Direct Marketing – Other Direct Marketers
    5970,  # Artist Supply and Craft Stores
    5971,  # Art Dealers and Galleries
    5972,  # Stamp and Coin Stores
    5973,  # Religious Goods Stores
    5975,  # Hearing Aids – Sales, Service, Supply Stores
    5976,  # Orthopedic Goods – Prosthetic Devices
    5977,  # Cosmetic Stores
    5978,  # Typewriter Stores – Sales, Rental, Service
    5983,  # Fuel – Fuel Oil, Wood, Coal, and Liquefied Petroleum
    5992,  # Florists
    5993,  # Cigar Stores and Stands
    5994,  # News Dealers and Newsstands
    5995,  # Pet Shops, Pet Foods, and Supplies Stores
    5996,  # Swimming Pools – Sales, Service, and Supplies
    5997,  # Electric Razor Stores – Sales and Service
    5998,  # Tent and Awning Shops
    5999   # Miscellaneous and Specialty Retail Stores
]

transit_mcc_codes = [
    4111,  # Local and Suburban Commuter Passenger Transportation, including Ferries
    4112,  # Passenger Railways
    4121,  # Taxicabs and Limousines
    4131,  # Bus Lines
    4784,  # Tolls and Bridge Fees
    7523,  # Parking Lots and Garages
    4011,  # Railroads (freight and passenger)
    4789   # Transportation Services – Not Elsewhere Classified
]

travel_mcc_codes = [
    3000,  # United Airlines
    3001,  # American Airlines
    3002,  # Pan American
    3003,  # Delta Airlines
    3004,  # Northwest Airlines
    3005,  # KLM
    3006,  # Scandinavian Airlines
    3007,  # Air France
    3008,  # Lufthansa
    3009,  # British Airways
    3010,  # Japan Airlines
    3011,  # Air Canada
    3012,  # Aeroflot
    3013,  # Qantas
    3014,  # Alaska Airlines
    3015,  # Southwest Airlines
    3016,  # U.S. Air Shuttle
    3017,  # Hawaiian Airlines
    3018,  # Alitalia
    3020,  # Aer Lingus
    3021,  # TAP Air Portugal
    3022,  # SAUDIA (Saudi Arabian Airlines)
    3023,  # Swissair
    3024,  # SAS
    3025,  # Varig Brazilian Airlines
    3026,  # Korean Air
    3027,  # Air India
    3028,  # Avianca
    3029,  # Iberia
    3030,  # Garuda Indonesia
    3031,  # Mexicana
    3032,  # Malaysian Airlines
    3033,  # LOT Polish Airlines
    3034,  # Philippine Airlines
    3035,  # Thai Airways
    3036,  # China Airlines
    3037,  # El Al Israel Airlines
    3038,  # Kuwait Airways
    3039,  # Ethiopian Airlines
    3040,  # EgyptAir
    3041,  # China Eastern Airlines
    3042,  # Emirates Airlines
    3043,  # Cathay Pacific
    3044,  # Singapore Airlines
    3045,  # Virgin Atlantic
    3046,  # Air New Zealand
    3051,  # Other International Airlines
    3061,  # Air Charter Services
    3075,  # Travel Agencies and Tour Operators
    3256,  # Timeshares
    3501,  # Lodging – Hotels, Motels, Resorts (commonly travel-related)
    4011,  # Railroads (including passenger transport)
    4111,  # Local and Suburban Commuter Passenger Transport
    4112,  # Passenger Railways
    4131,  # Bus Lines
    4411,  # Cruise Lines
    4511,  # Airlines and Air Carriers
    4722,  # Travel Agencies and Tour Operators
    4784,  # Tolls and Bridge Fees
    4789,  # Transportation Services – Not Elsewhere Classified
    5962,  # Direct Marketing – Travel-Related Arrangement Services
    7011,  # Lodging – Hotels, Motels, and Resorts
    7512,  # Car Rental Agencies
    7991,  # Tourist Attractions and Exhibits
    7996   # Amusement Parks, Carnivals, and Circuses (often related to travel activities)
]

category_to_mcc = {
    "dining": [5812, 5813, 5814, 5820, 5462],  # Restaurants and fast food
    "entertainment": entertainment_mcc_codes,  # Motion picture theaters, ticket agencies, sports promoters
    "gas": [4900, 5541, 5542, 5172, 9752],  # Gas/service stations
    "grocery": [5411, 5300, 5715, 5422, 5451],  # Grocery stores, meat provisioners, dairy
    "hotel": hotel_mcc_codes,  # Lodging and major hotel chains
    "onlineDining": [5815, 5816],  # Digital goods related to dining (e.g., meal kits)
    "onlineGrocery": [5961],  # Wholesale clubs, catalog merchants
    "rentalCar": rental_car_mcc_codes,  # Various car rental companies
    "retail": retail_mcc_codes,  # Sporting goods, department stores, specialty shops
    "streaming": [4899, 5815, 5968],  # Cable and pay TV, digital goods media
    "transit": transit_mcc_codes,  # Commuter passenger transport, railways, buses
    "travel": travel_mcc_codes  # Travel agencies, airlines, cruise lines
}

# Reversing the dictionary
mcc_to_category = {}
for category, mcc_list in category_to_mcc.items():
    for mcc in mcc_list:
        if mcc not in mcc_to_category:  # Only map the first encountered category
            mcc_to_category[mcc] = category

print(mcc_to_category)