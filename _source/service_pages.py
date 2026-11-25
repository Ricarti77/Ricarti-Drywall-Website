"""Individual service pages (Task 007). One data entry per page; every page uses the same structure.
All text is plain markup so the translation memory localizes it (PT now, ES/FR later)."""

AREAS = ['Toronto', 'Greater Toronto Area', 'Hamilton', 'Kitchener-Cambridge', 'Muskoka']

PAGES = [
dict(
 id='drywall', brands=True, num='01', url='/drywall-installation-toronto', short_name='Drywall Systems',
 title='Drywall Installation in Toronto and the GTA | Ricarti Drywall',
 desc='Drywall systems for custom homes, renovations and selected commercial interiors: walls, ceilings, bulkheads, Type X, moisture-resistant and multi-layer assemblies.',
 eyebrow='Service 01 · Drywall Systems', h1='Drywall, Installed <em>with Intent.</em>',
 lede='Every finish starts with how the board goes up. We plan layouts, joints and fastening so walls and ceilings are flat, solid and ready for an exceptional finish.',
 short='Ricarti Drywall installs drywall systems for custom homes, renovations and selected commercial interiors across Toronto, the GTA, Hamilton, Kitchener-Cambridge and Muskoka: walls, ceilings and bulkheads in standard, Type X fire-rated, moisture-resistant and tile-backer board, including multi-layer assemblies.',
 hero=('brule-05.jpg', 'Bright bedroom boarded floor to ceiling around a row of three windows, Brule', 'Brule — walls and ceiling boarded, ready for taping.'),
 intro_h='Flat, solid and <em>planned.</em>',
 intro=['Good drywall work is decided before the first sheet goes up. We review the framing, plan sheet layout to keep joints out of strong light, and choose the right board for each room: standard, fire-rated, moisture-resistant or tile backer.',
        'For builders, that means a clean, inspection-ready installation on schedule. For homeowners, it means walls and ceilings that look right for decades.'],
 caps=['Residential and selected commercial drywall installation', 'Custom homes and renovations', 'Walls, ceilings and bulkheads',
       'Multi-layer drywall assemblies', 'Custom and complex installations: curves, high ceilings and stair halls', 'Layouts planned to keep joints out of raking light'],
 materials=[('Standard 1/2-inch drywall', 'The everyday board for interior walls in most homes.'),
            ('5/8-inch Type X drywall', 'Fire-rated board used where a fire-resistance rating is required, such as garage separations and walls between units.'),
            ('Moisture-resistant drywall', 'For bathrooms, laundry rooms and basements where humidity is higher.'),
            ('DensShield tile backer', 'A glass-mat gypsum backer for tiled walls in wet areas.'),
            ('Multi-layer assemblies', 'Two or more layers of board for fire-rated or sound-rated walls and ceilings, built as specified.')],
 apps=['New custom homes', 'Additions and renovations', 'Basements', 'Bathrooms and laundry rooms', 'Garage separations and fire-rated walls', 'Selected commercial interiors'],
 benefits=[('A flatter finish', 'Careful layout and fastening mean fewer visible joints and less correction at the finishing stage.'),
           ('The right board in every room', 'Fire, moisture and tile requirements matched to the space and the drawings.'),
           ('One coordinated crew', 'Installation, taping and finishing by the same team, with no gap between trades.')],
 photos=[('brule-07.jpg', 'Room boarded around French doors, Brule', 'Brule — board around French doors.'),
         ('brule-03.jpg', 'Insulated ceiling on resilient channel with drywall stocked by type, Brule', 'Brule — board stocked by type before installation.'),
         ('kent-07.jpg', 'Open main floor during finishing with floors protected, Kent', 'Kent — open main floor during finishing.')],
 faqs=[('What thickness of drywall do you use?', 'Standard 1/2-inch board for most interior walls, and 5/8-inch Type X where a fire rating is required or where the drawings call for it. Ceilings and special assemblies follow the specification.'),
       ('Where is Type X drywall required?', 'Type X is used in fire-rated assemblies, for example between an attached garage and the house, or between units in semis and townhouses. The exact requirement comes from the drawings and the applicable building code.'),
       ('Do you install drywall in bathrooms?', 'Yes. We use moisture-resistant board on bathroom walls and ceilings, and DensShield or a similar tile backer behind tile where it is specified.'),
       ('Do you work on commercial projects?', 'We take on selected commercial interiors in addition to custom homes and residential projects. Send us the drawings to discuss your project.')],
 related=['finishing', 'framing', 'acoustic'],
),
dict(
 id='insulation', num='02', url='/insulation-spray-foam-toronto', short_name='Insulation & Spray Foam',
 title='Insulation and Spray Foam Contractor in Toronto | Ricarti Drywall',
 desc='Closed-cell spray foam, fibreglass and mineral wool batts, blown-in cellulose, attic insulation upgrades, vapour barrier and air sealing for homes across Toronto and the GTA.',
 eyebrow='Service 02 · Insulation &amp; Spray Foam', h1='Comfort, Built <em>into the Walls.</em>',
 lede='The right insulation, installed carefully and sealed properly, makes a home warmer, quieter and more efficient. We match each material to where it performs best.',
 short='Ricarti Drywall installs two-pound closed-cell spray foam, fibreglass and mineral wool batts and blown-in cellulose, upgrades attic insulation, and installs vapour barriers and air sealing for homes and builders across Toronto, the GTA, Hamilton, Kitchener-Cambridge and Muskoka. Required R-values depend on the project specifications, the building assembly and the applicable code.',
 hero=('brule-06.jpg', 'Closed-cell spray foam applied between roof rafters, Brule', 'Brule — closed-cell spray foam between roof rafters.'),
 intro_h='The layer you <em>never see.</em>',
 intro=['Insulation is the part of the wall that decides how a house feels in January. We install spray foam where it earns its cost, batts and blown-in insulation where they are the better value, and a continuous air and vapour barrier that your inspector can check before the board goes up.',
        'Insulation requirements and R-values depend on the project specifications, the building assembly and the applicable building code. We follow your designer’s energy specification and confirm the scope before work begins.'],
 caps=['Two-pound closed-cell spray foam', 'Fibreglass batt insulation', 'Mineral wool insulation', 'Attic insulation removal and upgrades',
       'Blown-in cellulose insulation', 'R-60 attic insulation applications where specified', 'Hybrid insulation systems', 'Vapour barrier and air-sealing solutions', 'Garage and exposed-floor insulation'],
 materials=[('Closed-cell spray foam (2 lb)', 'High insulating value per inch and an air seal in one; ideal for rim joists, sloped ceilings, below-grade walls and floors over garages.'),
            ('Fibreglass batts', 'Cost-effective insulation for standard wall cavities and open attic floors.'),
            ('Mineral wool batts', 'Dense, non-combustible insulation that also improves sound control.'),
            ('Blown-in cellulose', 'Loose-fill insulation for deep, even coverage of attic floors.'),
            ('Hybrid systems', 'Spray foam to seal and insulate critical areas, combined with batts or blown-in insulation elsewhere.'),
            ('Vapour barrier and air sealing', 'A continuous barrier on the warm side, with seams and penetrations sealed.')],
 apps=['Attic insulation upgrades', 'Rim joists and basements', 'Cathedral and sloped ceilings', 'Garage ceilings and floors over unheated spaces', 'Exterior walls in new homes and additions', 'Renovations of older homes'],
 benefits=[('Warmer in winter, cooler in summer', 'Fewer drafts and more even temperatures from room to room.'),
           ('Lower energy use', 'A well-sealed, well-insulated envelope reduces heating and cooling loads.'),
           ('Inspection-ready', 'Installed to your energy specification, with the air and vapour barrier ready for inspection.')],
 photos=[('stanton-04.jpg', 'Spray foam around a window opening, Stanton', 'Stanton — spray foam around a window opening.'),
         ('stanton-02.jpg', 'Mineral wool and steel channel on an exterior wall, Stanton', 'Stanton — mineral wool on an exterior wall.'),
         ('brule-03.jpg', 'Insulated walls and ceiling before drywall, Brule', 'Brule — insulated walls and ceiling before board.')],
 faqs=[('What R-value do I need?', 'It depends on the project specifications, the building assembly and the applicable building code. For new homes, the values come from the designer’s energy specification. R-60 is a common target for attic insulation where the energy design calls for it.'),
       ('Is spray foam better than batts?', 'Each has its place. Closed-cell spray foam works best in tight or moisture-prone areas such as rim joists, sloped ceilings and below-grade walls; batts and blown-in insulation are often the better value in standard walls and open attics. <a href="/journal/spray-foam-vs-batt-insulation">Read our guide</a>.'),
       ('Can you remove old attic insulation?', 'Yes. We remove old or damaged attic insulation, seal air leaks and install new insulation to the level your project calls for.'),
       ('Do you install the vapour barrier?', 'Yes. We install the vapour barrier and seal seams and penetrations so the assembly is ready for inspection before drywall.')],
 related=['acoustic', 'drywall', 'framing'],
),
dict(
 id='finishing', num='03', url='/drywall-finishing-toronto', short_name='Level 4 &amp; Level 5 Finishing',
 title='Drywall taping and finishing in Toronto: Level 4 vs Level 5 | Ricarti Drywall',
 desc='The six drywall finish levels in plain words, when a Level 5 skim coat is worth paying for, and what should be in a finishing quote. Toronto and the GTA.',
 eyebrow='Service 03 · Level 4 &amp; Level 5 Finishing', h1='Surfaces Ready for <em>the Light.</em>',
 lede='Finishing is where a wall becomes beautiful or ordinary. We tape, coat and sand to the level each room needs, with a full skim coat where light and paint demand it.',
 short='Ricarti Drywall finishes painted walls to Level 4 as standard and recommends Level 5, a full skim coat, where strong side light, tall walls, or dark or glossy paint would show the joints. We also remove popcorn ceilings, create smooth ceiling finishes and repair drywall and plaster. The finish level for each room is written into the estimate.',
 hero=('kent-01.jpg', 'Smooth painted walls and ceiling in a finished bedroom with white oak floors, Kent', 'Kent — smooth painted walls and ceiling.'),
 intro_h='Level 4 or <em>Level 5?</em>',
 intro=['<b>Level 4</b> is three coats of joint compound over taped joints and fasteners, sanded smooth. It suits most painted rooms with flat or eggshell paint.',
        '<b>Level 5</b> adds a thin skim coat over the entire surface. It evens out the difference between paper and compound, so joints do not show under raking light, on tall walls, or beneath dark or glossy paint. We recommend it only where it pays, and say so room by room.'],
 caps=['Professional drywall taping', 'Level 4 finishing', 'Level 5 finishing', 'Full-surface skim coating', 'Smooth ceiling finishes',
       'Popcorn ceiling removal', 'Drywall repairs and restoration', 'Premium paint-ready surfaces', 'Finishing for critical lighting conditions'],
 materials=[('Paper and mesh joint tape', 'Chosen for each joint type, embedded in compound for a strong, crack-resistant seam.'),
            ('Joint compounds', 'Setting-type and ready-mix compounds used where each performs best.'),
            ('Corner beads', 'Paper-faced, metal or vinyl beads for straight, durable corners.'),
            ('Skim coat', 'A thin coat over the entire surface for Level 5 finishes.'),
            ('Primer-ready surfaces', 'Sanded, cleaned and checked under a work light before paint.')],
 apps=['Living rooms and great rooms with large windows', 'Foyers and stair halls', 'Ceilings under pot lights and skylights', 'Rooms with dark or glossy paint', 'Popcorn ceiling removal and smooth ceilings', 'Repairs in older homes'],
 benefits=[('A finish that disappears', 'Walls and ceilings that read as flat, clean planes in any light.'),
           ('Honest recommendations', 'Level 5 only where light or paint will show the joints; Level 4 where it is enough.'),
           ('Checked before paint', 'Every surface inspected with a work light held flat to the wall.')],
 extra='levels',
 photos=[('kent-05.jpg', 'Bedroom with finish coats of joint compound on walls and ceiling, floors protected, Kent', 'Kent — finish coats, floors protected.'),
         ('lauther-02.jpg', 'New ceiling taped around an original plaster medallion, Lauther Ave', 'Lauther Ave — new ceiling around the original medallion.'),
         ('thompson-01.jpg', 'Finisher on stilts skimming a ceiling with floors covered, Thompson', 'Thompson — skimming a ceiling.')],
 faqs=[('How much more does Level 5 cost than Level 4?', 'Level 5 adds a full coat of compound and the labour to sand it, so it costs more on the finishing line. Using it only where the light demands it keeps the cost down. Your estimate shows the finish level for each room.'),
       ('Can I tell the finish level by looking?', 'Hold a bright light flat against the wall, or look along it toward a window. Joints and screw heads that disappear face-on often show at that angle. It is how we check our own work.'),
       ('Can you remove popcorn ceilings?', "Yes. Textured ceilings can be removed and refinished smooth, or covered with new drywall. Ceilings installed before the 1990s may contain asbestos. In Ontario, asbestos on construction projects is regulated under Ontario Regulation 278/05, which requires material that may contain asbestos to be identified before it is disturbed. We have the texture tested before any removal and plan the work around the result."),
       ('Do you finish drywall hung by another company?', 'Yes, after we have looked at it. Poorly hung board costs more to finish well, and we will say so in the estimate.')],
 related=['architectural', 'drywall', 'acoustic'],
),
dict(
 id='architectural', brands=True, num='04', url='/architectural-drywall-finishing-toronto', short_name='Architectural Finishing',
 title='Architectural Drywall Finishing in Toronto: Curves, Reveals and Trimless Details | Ricarti Drywall',
 desc='Curved walls and ceilings, arched openings, shadow reveals, Z-reveals, trimless details, flush vents and frameless lighting details in drywall for premium homes.',
 eyebrow='Service 04 · Architectural Finishing', h1='Where Drywall Becomes <em>Architecture.</em>',
 lede='Curves, reveals and trimless details turn drywall into a design element. They demand precise framing, the right profiles and a meticulous finish, and that is where we focus.',
 short='Ricarti Drywall builds and finishes architectural drywall details for premium homes across Toronto and the GTA: curved walls and ceilings, arched openings, shadow reveals and Z-reveals, trimless door and window returns within our drywall scope, flush-mounted vents, frameless lighting details and specialized corner and butt-joint systems.',
 hero=('brule-09.jpg', 'Arched doorway with corner bead opening onto an arched window, Brule', 'Brule — arched doorway with corner bead.'),
 intro_h='Details that <em>define a room.</em>',
 intro=['In a minimalist interior there is nowhere to hide. A shadow reveal must be perfectly straight, a curve must be true from every angle, and a vent or light must sit exactly flush with the ceiling. We plan these details with the designer and builder, use purpose-made profiles, and finish them by hand.',
        'Trimless doors and windows are part of our work where they fall within the drywall scope: the drywall returns, beads and reveals around the opening. Frames, hardware and glazing remain with the other trades.'],
 caps=['Curved walls and ceilings', 'Arched openings', 'Architectural shadow reveals', 'Z-reveal profiles', 'Trimless doors and windows within our drywall scope',
       'Flush-mounted vent systems, including Aria Vent and Envisivent', 'Frameless recessed lighting details', 'Trim-Tex architectural profiles',
       'Buttboard butt-joint systems', 'Specialized corner bead systems', 'Prefabricated drywall details', 'Custom architectural drywall applications'],
 materials=[('Reveal and Z-reveal profiles', 'Create crisp shadow lines where walls meet ceilings, floors or other materials.'),
            ('Trim-Tex architectural profiles', 'Vinyl beads and profiles for reveals, curves, arches and trimless edges.'),
            ('Aria Vent and Envisivent', 'Flush-mount vents set into the drywall and finished with joint compound, so supply and return vents sit flush with the surface.'),
            ('Frameless lighting details', 'Recessed fixtures and trims designed to be finished flush with the ceiling.'),
            ('Buttboard drywall backer', 'An engineered backer that pulls cut drywall ends into a slight taper, for flatter butt joints on walls and ceilings.'),
            ('Specialized corner beads', 'Bullnose, flexible arch and custom beads for durable, precise edges.')],
 apps=['Minimalist and contemporary interiors', 'Feature ceilings and coffers', 'Arched openings and niches', 'Curved stairs and walls', 'Trimless doors and windows', 'Clean, flush vents and lighting'],
 benefits=[('A cleaner interior', 'Fewer visible trims and grilles, and more of the architecture.'),
           ('Precision you can see', 'Straight reveals, true curves and flush details from every angle.'),
           ('Coordinated with your design team', 'Details planned with the architect, designer and builder before installation.')],
 photos=[('brule-01.jpg', 'Barrel-vaulted dormer nook boarded in moisture-resistant drywall, Brule', 'Brule — barrel-vaulted dormer nook.'),
         ('brule-04.jpg', 'Arched doorway boarded with corner bead, Brule', 'Brule — arched doorway.'),
         ('brule-08.jpg', 'Arched niche and framing before board, Brule', 'Brule — arched niche before board.')],
 faqs=[('What is a shadow reveal?', 'A small recessed gap, formed with a metal or vinyl profile, where a wall meets the ceiling, floor or another material. It replaces trim with a clean shadow line.'),
       ('Do you install trimless doors and windows?', 'We build the drywall portion of trimless openings: the returns, beads and reveals around the frame. Door frames, hardware, windows and glazing are handled by the other trades.'),
       ('Can flush vents be added to an existing ceiling?', 'Often, yes, depending on the duct and ceiling construction. Flush-mount vents such as Aria Vent and Envisivent are set into the drywall and finished with joint compound. Your HVAC contractor confirms the duct sizes and airflow.'),
       ('Do you work with designers and architects?', 'Yes. Architectural details work best when they are planned with the design team before framing and installation.')],
 related=['finishing', 'drywall', 'framing'],
),
dict(
 id='acoustic', brands=True, num='05', url='/soundproofing-toronto', short_name='Acoustic &amp; Soundproofing',
 title='Soundproofing and Acoustic Drywall Systems in Toronto | Ricarti Drywall',
 desc='Sound-control assemblies for bedrooms, bathrooms, home offices, media rooms and selected commercial spaces: ROCKWOOL Safe’n’Sound, QuietZone, SONOpan, resilient channel and multi-layer drywall.',
 eyebrow='Service 05 · Acoustic &amp; Soundproofing', h1='Quiet, by <em>Design.</em>',
 lede='A quieter room comes from the right combination of mass, decoupling, absorption and sealing. We build sound-control assemblies into walls and ceilings, and tell you honestly what each upgrade can do.',
 short='Ricarti Drywall builds sound-control walls and ceilings for bedrooms, bathrooms, home offices, entertainment rooms and selected commercial spaces across Toronto and the GTA, using mineral wool and acoustic batts such as ROCKWOOL Safe’n’Sound and Owens Corning QuietZone, SONOpan panels, resilient channel and multi-layer drywall. Performance depends on the full assembly, including how it is sealed.',
 hero=('stanton-05.jpg', 'Mineral wool sound insulation behind steel resilient channel on a sloped ceiling, Stanton', 'Stanton — mineral wool and resilient channel under a sloped ceiling.'),
 intro_h='Absorption or <em>isolation?</em>',
 intro=['<b>Sound absorption</b> reduces echo and reverberation inside a room. Acoustic panels and soft finishes do this, but they do little to stop sound passing through a wall.',
        '<b>Sound isolation</b> stops sound travelling from one space to another. It comes from the wall or ceiling assembly itself: mass, decoupling, absorptive insulation in the cavity, and airtight sealing. Soundproofing a room is mostly about isolation, and that is what we build.'],
 caps=['Mineral wool acoustic insulation', 'ROCKWOOL Safe’n’Sound', 'Owens Corning QuietZone acoustic batts', 'SONOpan soundproofing panels',
       'Resilient channels', 'Multi-layer drywall systems', 'Acoustic sealing of perimeters and penetrations'],
 materials=[('ROCKWOOL Safe’n’Sound', 'Stone wool batts for interior walls and floors that add sound absorption in the cavity and fire resistance.'),
            ('Owens Corning QuietZone', 'Acoustic fibreglass batts designed to reduce noise transfer through interior walls, floors and ceilings.'),
            ('SONOpan panels', 'Soundproofing panels made from recycled wood fibre, installed under drywall as part of a sound-control assembly.'),
            ('Resilient channel', 'Metal channel that decouples drywall from the framing, reducing vibration transfer.'),
            ('Multi-layer drywall', 'Additional layers of board to add mass to walls and ceilings.'),
            ('Acoustic sealant', 'Flexible sealant at perimeters, outlets and penetrations, where sound would otherwise leak.')],
 apps=['Bedrooms and nurseries', 'Bathrooms', 'Home offices', 'Media and entertainment rooms', 'Basement suites and shared walls', 'Selected commercial spaces'],
 benefits=[('Better sleep and focus', 'Quieter bedrooms and offices, less noise from bathrooms and shared spaces.'),
           ('Built into the structure', 'Sound control inside the wall or ceiling, not added on the surface.'),
           ('Honest expectations', 'Clear advice on what each upgrade can achieve in your home.')],
 photos=[('stanton-03.jpg', 'Mineral wool insulation behind steel resilient channel, Stanton', 'Stanton — mineral wool behind resilient channel.'),
         ('svc-acoustic-480.jpg', 'A long wall of mineral wool sound insulation behind steel resilient channels, Stanton', 'Stanton — mineral wool and resilient channel along a shared wall.'),
         ('stanton-02.jpg', 'Steel channel and mineral wool on a wall, Stanton', 'Stanton — channel and mineral wool before board.')],
 faqs=[('What is the difference between sound absorption and sound isolation?', 'Absorption reduces echo inside a room; isolation stops sound passing between rooms. Soundproofing a wall or ceiling is mostly about isolation, which comes from mass, decoupling, cavity insulation and sealing.'),
       ('What STC rating will my wall achieve?', 'STC ratings come from laboratory tests of complete, specified assemblies. We build assemblies as specified, but we do not promise a particular rating unless the exact tested assembly is being built. Real-world results also depend on flanking paths, doors and openings.'),
       ('Can you soundproof an existing room?', 'Yes. Common upgrades add acoustic insulation, resilient channel or SONOpan and an extra layer of drywall, with every gap sealed. <a href="/journal/soundproofing-a-room">Read our soundproofing guide</a>.'),
       ('Does insulation alone soundproof a wall?', 'It helps, but on its own the improvement is modest. The best results combine insulation with added mass, decoupling and careful sealing.')],
 related=['insulation', 'drywall', 'framing'],
),
dict(
 id='framing', num='06', url='/metal-stud-framing-toronto', short_name='Metal Stud Framing',
 title='Metal Stud Framing for Homes and Interiors in Toronto | Ricarti Drywall',
 desc='Non-load-bearing steel stud partitions, ceiling framing, bulkheads and dropped ceilings for custom homes, renovations and selected commercial interiors.',
 eyebrow='Service 06 · Metal Stud Framing', h1='Straight, True <em>and Ready for Board.</em>',
 lede='Light-gauge steel framing gives straight walls, true ceilings and precise details. We frame non-load-bearing partitions, ceilings and bulkheads, and coordinate them with the insulation and drywall that follow.',
 short='Ricarti Drywall frames non-load-bearing steel stud partitions, ceilings, bulkheads and dropped ceilings for custom homes, renovations and selected commercial interiors across Toronto and the GTA, coordinated with the drywall, insulation and acoustic assemblies. We do not provide structural steel framing.',
 hero=('brule-03.jpg', 'Steel channel ceiling grid installed over insulation before board, Brule', 'Brule — steel channel ceiling grid before board.'),
 intro_h='The frame behind <em>a flawless finish.</em>',
 intro=['Steel studs and track are straight, dimensionally stable and do not shrink or twist, which makes them ideal for interior partitions, basements, ceilings and the bulkheads that hide ducts and pipes.',
        'Because we also install the insulation, drywall and acoustic layers, the framing is planned for what comes next: backing where it is needed, openings in the right place, and a flat plane for the finish.'],
 caps=['Non-load-bearing steel stud partitions', 'Residential and commercial interior framing', 'Metal stud and track systems', 'Ceiling framing',
       'Bulkheads and dropped ceilings', 'Custom framing details', 'Coordination with drywall, insulation and acoustic assemblies'],
 materials=[('Steel studs and track', 'Light-gauge, non-load-bearing studs and track for interior partitions.'),
            ('Furring channel', 'For ceilings and for straightening or furring out existing walls.'),
            ('Resilient channel', 'Used where walls and ceilings need sound isolation.'),
            ('Backing and blocking', 'Installed where cabinets, fixtures and accessories will be mounted.')],
 apps=['Basement walls and partitions', 'Bulkheads for ducts and plumbing', 'Dropped and feature ceilings', 'Interior partitions in renovations', 'Selected commercial interiors', 'Framing for architectural details'],
 benefits=[('Straight walls and ceilings', 'Steel does not shrink, warp or twist, so the drywall plane stays flat.'),
           ('Fewer trades, better coordination', 'Framing, insulation and drywall planned and installed by one team.'),
           ('Ready for what comes next', 'Backing and openings in place before the board goes up.')],
 photos=[('stanton-02.jpg', 'Steel channel and mineral wool on a wall, Stanton', 'Stanton — steel channel over mineral wool.'),
         ('stanton-01.jpg', 'Open floor with exposed joists and a timber staircase before insulation and board, Stanton', 'Stanton — open floor before framing details and board.'),
         ('brule-08.jpg', 'Arched niche and framing before board, Brule', 'Brule — framing for an arched niche.')],
 faqs=[('Do you do structural steel framing?', 'No. We frame non-load-bearing steel stud partitions, ceilings and bulkheads. Structural framing is designed by an engineer and built by other trades.'),
       ('Why choose metal studs over wood?', 'Steel studs are straight and dimensionally stable, do not shrink or twist, and are well suited to interior partitions, basements, ceilings and bulkheads.'),
       ('Can you frame bulkheads around ducts and pipes?', 'Yes. We frame bulkheads and dropped ceilings to conceal ductwork and plumbing, coordinated with your mechanical layout.'),
       ('Do you frame basements?', 'Yes. We frame basement walls and partitions, then insulate and drywall them, ready for paint.')],
 related=['drywall', 'acoustic', 'insulation'],
),
]

BY_ID = {p['id']: p for p in PAGES}

LEVELS = [('0', 'Board hung. No tape or compound.', 'Temporary walls'), ('1', 'Tape set in compound at joints.', 'Hidden areas, above ceilings'),
          ('2', 'Tape plus one coat over joints and screws.', 'Garages, under tile'), ('3', 'A second coat over joints and screws.', 'Under heavy texture'),
          ('4', 'A third coat, sanded smooth.', 'Most painted rooms: flat and eggshell paint'), ('5', 'Level 4 plus a skim coat over the whole surface.', 'Raking light, tall walls, curved walls, glossy or dark paint')]

def img(src, alt, w=900, h=1600, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    if src.endswith('-480.jpg'):
        w, h = 480, 600
    return '<img src="/images/%s" alt="%s" width="%d" height="%d" %s>' % (src, alt, w, h, load)

def body(p):
    caps = ''.join('<li>%s</li>' % c for c in p['caps'])
    mats = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in p['materials'])
    apps = ''.join('<li>%s</li>' % a for a in p['apps'])
    ben = ''.join('<li><span class="rd-b-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, h, d) for i, (h, d) in enumerate(p['benefits']))
    photos = ''.join('<figure>%s<figcaption class="rd-cap">%s</figcaption></figure>' % (img(f, alt), cap) for f, alt, cap in p['photos'])
    faq = ''.join('<details%s><summary>%s<span class="rd-plus" aria-hidden="true">+</span></summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(p['faqs']))
    rel = ''.join('<li><a href="%s"><span class="rd-b-n">%s</span><span class="rd-s-rel-h">%s</span><span class="rd-s-rel-c">Explore Service<span aria-hidden="true"> →</span></span></a></li>' % (BY_ID[r]['url'], BY_ID[r]['num'], BY_ID[r]['short_name']) for r in p['related'])
    paras = ''.join('<p>%s</p>' % x for x in p['intro'])
    extra = ''
    if p.get('extra') == 'levels':
        rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in LEVELS)
        extra = '''<section class="rd-wrap rd-sec" aria-labelledby="levels-h"><div class="rd-s-two"><div><p class="rd-kicker">The finish levels</p><h2 id="levels-h" class="rd-h2">The six finish levels, <em>in plain words.</em></h2>
<p class="rd-muted" style="margin:20px 0 0;max-width:420px">The industry grades drywall finish from Level 0 to Level 5. Naming the level in the contract makes sure “paint-ready” means the same thing to you and to us.</p></div>
<div class="rd-s-table"><table><thead><tr><th>Level</th><th>What is done</th><th>Where it is used</th></tr></thead><tbody>%s</tbody></table></div></div></section>''' % rows
    return '''<main id="main">
<div class="rd-wrap">
<nav aria-label="Breadcrumb" class="rd-muted" style="font-size:13px;padding-top:28px"><a href="/">Home</a> / <a href="/#services">Services</a> / %(short_name)s</nav>
<section class="rd-cover rd-b-hero rd-s-hero" aria-label="Introduction">
<div class="rd-cover-txt">
<p class="rd-eyebrow">%(eyebrow)s</p>
<h1><span class="rd-display">%(h1)s</span></h1>
<p class="rd-lede">%(lede)s</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate">Request an Estimate</a><a class="rd-btn-o" href="/estimate?type=builder">Builders — Send Your Drawings</a></div>
<div class="rd-short rd-b-short"><b>IN SHORT</b>%(short)s</div>
</div>
<figure>%(hero)s<figcaption class="rd-cap">%(hero_cap)s</figcaption></figure>
</section>
</div>

<section class="rd-wrap rd-sec" aria-labelledby="intro-h">
<div class="rd-s-two"><div><p class="rd-kicker">The service</p><h2 id="intro-h" class="rd-h2">%(intro_h)s</h2></div><div class="rd-s-prose">%(paras)s</div></div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="caps-h">
<div class="rd-s-two"><div><p class="rd-kicker">Technical capabilities</p><h2 id="caps-h" class="rd-h2">What we <em>deliver.</em></h2></div><ul class="rd-s-caps">%(caps)s</ul></div>
</section>
%(extra)s
<section class="rd-wrap rd-sec" aria-labelledby="mat-h">
<div class="rd-s-two"><div><p class="rd-kicker">Materials and systems</p><h2 id="mat-h" class="rd-h2">The right system <em>for the job.</em></h2>
%(note)s</div>
<dl class="rd-s-mats">%(mats)s</dl></div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="apps-h">
<div class="rd-s-apps"><div><p class="rd-kicker">Typical applications</p><h2 id="apps-h" class="rd-h2">Where it <em>makes the difference.</em></h2><ul class="rd-s-applist">%(apps)s</ul></div>
<div class="rd-s-photos">%(photos)s</div></div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="ben-h">
<header class="rd-exp-head"><div><p class="rd-kicker">Benefits</p><h2 id="ben-h" class="rd-h2">Why it <em>matters.</em></h2></div></header>
<ol class="rd-b-grid">%(ben)s</ol>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="faq-h">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:40px 64px;align-items:start">
<div><p class="rd-kicker">Questions</p><h2 id="faq-h" class="rd-h2">Frequently asked.</h2></div>
<div class="rd-faq" style="border-top:1px solid var(--hair)">%(faq)s</div>
</div>
</section>

<section class="rd-wrap rd-sec" aria-labelledby="rel-h">
<p class="rd-kicker">Related services</p><h2 id="rel-h" class="rd-h2" style="font-size:clamp(28px,3vw,40px)">Explore more of <em>what we do.</em></h2>
<ul class="rd-s-rel">%(rel)s</ul>
</section>
</main>

<section class="rd-b-cta" aria-labelledby="cta-h"><div>
<div class="rd-b-cta-l">
<p class="rd-kicker">Start a project</p>
<h2 id="cta-h">Let's Talk About <em>Your Project.</em></h2>
<p class="rd-b-cta-p">Homeowners: request an estimate and we will arrange a visit. Builders and architects: send your drawings and we will review the scope.</p>
<div class="rd-cover-cta"><a class="rd-btn" href="/estimate">Request an Estimate</a><a class="rd-btn-o" href="/estimate?type=builder">Builders — Send Your Drawings</a></div>
<p class="rd-b-contact"><a href="tel:+16474821139">(647) 482-1139</a><a href="mailto:cris@ricartidrywall.ca">cris@ricartidrywall.ca</a></p>
</div>
<div class="rd-b-cta-r"><h3>Service area</h3><dl>%(areas)s</dl></div>
</div></section>
''' % dict(p, hero=img(p['hero'][0], p['hero'][1], eager=True), hero_cap=p['hero'][2], paras=paras, caps=caps, mats=mats, apps=apps, photos=photos,
           ben=ben, faq=faq, rel=rel, extra=extra, note=('<p class="rd-muted rd-s-note">Product names are used to describe the systems we install. Ricarti Drywall has no official partnership or distribution agreement with these manufacturers.</p>' if p.get('brands') else ''), areas=''.join('<div><dt>%s</dt><dd></dd></div>' % a for a in AREAS))

CSS = '''
.rd-s-hero .rd-display{font-size:clamp(44px,5.8vw,92px)}
.rd-s-two{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:32px clamp(40px,6vw,104px);align-items:start}
.rd-s-prose p{margin:0 0 18px;font-size:18px;line-height:1.7;color:var(--ink);max-width:680px}
.rd-s-prose b{font-weight:600}
.rd-s-caps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;border-top:1px solid var(--ink)}
.rd-s-caps li{padding:15px 0 15px 22px;border-bottom:1px solid var(--hair);font:300 clamp(18px,1.5vw,21px)/1.35 var(--serif);position:relative}
.rd-s-caps li::before{content:"";position:absolute;left:0;top:25px;width:8px;height:1px;background:var(--spruce)}
.rd-s-mats{margin:0;border-top:1px solid var(--ink)}
.rd-s-mats>div{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:8px 32px;padding:18px 0;border-bottom:1px solid var(--hair)}
.rd-s-mats dt{font:300 clamp(19px,1.6vw,22px)/1.3 var(--serif)}
.rd-s-mats dd{margin:0;font-size:15px;line-height:1.6;color:var(--muted)}
.rd-s-note{font-size:13px;margin:24px 0 0;max-width:380px}
.rd-s-apps{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px clamp(40px,6vw,96px);align-items:start}
.rd-s-applist{list-style:none;margin:28px 0 0;padding:0;border-top:1px solid var(--hair)}
.rd-s-applist li{padding:12px 0;border-bottom:1px solid var(--hair);font-size:16px}
.rd-s-photos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.rd-s-photos figure{margin:0}
.rd-s-photos img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.rd-s-table{overflow-x:auto}
.rd-s-table table{width:100%;border-collapse:collapse;font-size:15px}
.rd-s-table th{text-align:left;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:500;color:var(--muted);padding:0 16px 12px 0;border-bottom:1px solid var(--ink)}
.rd-s-table td{padding:14px 16px 14px 0;border-bottom:1px solid var(--hair);vertical-align:top}
.rd-s-table td:first-child{font:300 28px/1 var(--serif);color:var(--spruce);width:64px}
.rd-s-rel{list-style:none;margin:32px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px 32px}
.rd-s-rel a{display:block;text-decoration:none;border-top:1px solid var(--ink);padding-top:18px}
.rd-s-rel-h{display:block;font:300 clamp(22px,2vw,28px)/1.15 var(--serif);margin:10px 0 14px}
.rd-s-rel-c{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;color:var(--spruce)}
.rd-s-rel a:hover .rd-s-rel-h{color:var(--spruce)}
.rd-b-cta-r dl>div:has(dd:empty){grid-template-columns:1fr}
@media (max-width:900px){.rd-s-two,.rd-s-apps{grid-template-columns:1fr}.rd-s-rel{grid-template-columns:1fr}}
@media (max-width:640px){.rd-s-caps{grid-template-columns:1fr}.rd-s-photos{grid-template-columns:1fr 1fr}.rd-s-photos figure:nth-child(3){display:none}.rd-s-mats>div{grid-template-columns:1fr}}
'''
