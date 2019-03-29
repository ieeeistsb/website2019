# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from app.models import Volunteer, Community, Projects, Team, TeamMember, SocialNetwork, Tag
import os
from django.conf import settings
from django.core.files import File

init_folder = os.path.join(settings.MEDIA_ROOT, "init")
init_img = os.path.join(init_folder, "img")
communities_folder = os.path.join(init_img, "communities")
volunteers_folder = os.path.join(init_img, "volunteers")
projects_folder = os.path.join(init_img, "projects")


def init_communities():
    communities = [
        {"name": "Computer Society", "info": "This is CS's gorgeous info.",
         "image": File(open(os.path.join(communities_folder, 'CS.png'), 'r')),
         "chair": [Volunteer.objects.get(ieee_contact="diogomesquita@ieee-ist.org")],
         "vice_chair": [Volunteer.objects.get(ieee_contact="alexignatiev@ieee-ist.org"),
                        Volunteer.objects.get(ieee_contact="afonsocaetano@ieee-ist.org")]
         },
        {"name": "Engineering in Medicine & Biology Society", "info": "This is EMBS...", "image": "",
         "chair": [Volunteer.objects.get(ieee_contact="joaocarvalho@ieee-ist.org")],
         "vice_chair": [Volunteer.objects.get(ieee_contact="catiafortunato@ieee-ist.org"),
                        Volunteer.objects.get(ieee_contact="barbaracosta@ieee-ist.org")]
         },
        {"name": "Robotics and Automation Society", "info": "We build this. And that.",
         "image": File(open(os.path.join(communities_folder, 'RAS.png'), 'r')),
         "chair": [Volunteer.objects.get(ieee_contact="andrelopes@ieee-ist.org")],
         "vice_chair": [Volunteer.objects.get(ieee_contact="quevinjagmohandas@ieee-ist.org")]
         },
        {"name": "Women in Engineering", "info": "Dedicated to promoting women engineers and scientists.",
         "image": File(open(os.path.join(communities_folder, 'WIE.png'), 'r')),
         "chair": [Volunteer.objects.get(ieee_contact="ritabarreiros@ieee-ist.org")]
         },
        {"name": "Industry Applications Society",
         "info": "Dedicated to promoting women engineers and scientists.",
         "image": File(open(os.path.join(communities_folder, 'IAS.png'), 'r')),
         "chair": [Volunteer.objects.get(ieee_contact="andrepires@ieee-ist.org")]}]

    relations = {
        "Computer Society": 'cs.md',
        "Engineering in Medicine & Biology Society": 'embs.md',
        "Robotics and Automation Society": 'ras.md',
        "Industry Applications Society": 'ias.md',
        "Women in Engineering": 'wie.md'
    }

    for c in communities:
        chairs = c.pop("chair", [])
        vice_chairs = c.pop("vice_chair", [])
        co = Community.objects.update_or_create(**c)[0]
        co.info = open(os.path.join(settings.BASE_DIR, 'markdowns', 'en', relations[co.name])).read()
        co.info_pt = open(os.path.join(settings.BASE_DIR, 'markdowns', 'pt', relations[co.name])).read()
        for chair in chairs:
            co.chair.add(chair)
        for vc in vice_chairs:
            co.vice_chair.add(vc)
        co.save()
        Tag.objects.create(name=co.get_tagname())


def init_volunteers():
    volunteers = [
        {"name": "Diogo Monteiro", "ieee_contact": "diogomonteiro@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'diogo_monteiro.jpg'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/diogo.monteiro.58",
              "linkedin": "https://pt.linkedin.com/pub/diogo-monteiro/72/324/18b"}
         },
        {"name": "Pedro Reganha", "ieee_contact": "pedroreganha@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'pedro_reganha.jpg'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/pedro.reganha",
              "linkedin": "www.linkedin.com/in/pedroreganha"}
         },
        {"name": "André Lopes", "ieee_contact": "andrelopes@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'andre_lopes.jpg'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/andre.rodrigues.lopes1",
              "linkedin": "https://www.linkedin.com/in/andré-lopes-45ba16a4"}
         },
        {"name": "Rui Santos", "ieee_contact": "ruisantos@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'rui_santos.jpg'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/ruipds",
              "linkedin": "https://www.linkedin.com/in/ruipds"}
         },
        {"name": "Inês Ferreira", "ieee_contact": "inesferreira@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'ines_ferreira.jpg'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/ines.ferreira.54738",
              "linkedin": "https://www.linkedin.com/in/inesjorgeferreira"}
         },
        {"name": "Diogo Mesquita", "ieee_contact": "diogomesquita@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'diogo_mesquita.png'), 'r'))
         },
        {"name": "João Apura", "ieee_contact": "joaoapura@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joao_apura.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/joao.apura",
              "linkedin": "https://pt.linkedin.com/in/joaoapura/en"}
         },
        {"name": "Rúben Capitão", "ieee_contact": "rubencapitao@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'ruben_capitao.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/ruben.capitao.1"}
         },
        {"name": "Rita Barreiros", "ieee_contact": "ritabarreiros@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'rita_barreiros.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/rita.barreiros.31",
              "linkedin": "https://pt.linkedin.com/in/rita-barreiros-58a62b10b/en"}
         },
        {"name": "André Pires", "ieee_contact": "andrepires@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'andre_pires.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/andre.p.pires",
              "linkedin": "https://pt.linkedin.com/in/andreppires/en"}
         },
        {"name": "Sofia Ferreira", "ieee_contact": "sofiaferreira@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'sofia_ferreira.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/sofia.ferreira.18041",
              "linkedin": "https://pt.linkedin.com/pub/sofia-ferreira/75/856/483/en"}
         },
        {"name": "Joana Pereira", "ieee_contact": "joanapereira@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joana_pereira.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/joanapereira94",
              "linkedin": "https://pt.linkedin.com/pub/joana-pereira/b7/304/bab/en"}
         },
        {"name": "João Santos", "ieee_contact": "joaosantos@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joao_santos.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/jsantos15"}
         },
        {"name": "Anisa Shahidian", "ieee_contact": "anisashahidian@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'anisa.png'), 'r'))},
        {"name": "Ana Colaço", "ieee_contact": "anacolaco@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'ana_colaco.png'), 'r')),
         "socials":
             {"facebook": "https://www.facebook.com/ana.colaco23"}
         },
        {"name": "João Pedro Boavida", "ieee_contact": "counselor@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joao_boavida.png'), 'r'))},
        {"name": "Bruno Machado", "ieee_contact": "brunomachado@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'bruno_machado.png'), 'r'))},
        {"name": "João Carvalho", "ieee_contact": "joaocarvalho@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joao_carvalho.png'), 'r'))},
        {"name": "Alexandr Ignatiev", "ieee_contact": "alexignatiev@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'alex_ignatiev.jpg'), 'r'))},
        {"name": "Afonso Caetano", "ieee_contact": "afonsocaetano@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'afonso_caetano.jpg'), 'r'))},
        {"name": "Bárbara Costa", "ieee_contact": "barbaracosta@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'barbara_costa.png'), 'r'))},
        {"name": "Cátia Fortunato", "ieee_contact": "catiafortunato@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'catia_fortunato.jpg'), 'r'))},
        {"name": "Quevin Jagmohandas", "ieee_contact": "quevinjagmohandas@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'quevin.jpg'), 'r'))},

        {"name": "Diogo Barradas", "ieee_contact": "diogobarradas@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'diogo_barradas.jpg'), 'r'))},
        {"name": "Pedro Freire", "ieee_contact": "pedrofreire@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'pedro_freire.jpg'), 'r'))},
        {"name": "Joana Palhinha", "ieee_contact": "joanapalhinha@ieee-ist.org",
         "image": File(open(os.path.join(volunteers_folder, 'joana_palhinha.jpg'), 'r'))},

        {"name": "Catarina Martins"},
        {"name": "Gonçalo Carito"},
        {"name": "Paula Monteiro"},
        {"name": "Francisco Esteves"},
        {"name": "Diana Rodrigues"},
        {"name": "Francisco Dias"},
        {"name": "Rui Rocha"},
        {"name": "Carmo Póvoa"},
        {"name": "Rui Costa"},
        {"name": "Ricardo Câncio Silva"},
        {"name": "Gonçalo Carito"},
        {"name": "Fábio Domingos"},
        {"name": "João Azevedo"},
        {"name": "Giovanna Franchi"},
        {"name": "Camille Coyac"},
        {"name": "Inês Fernandes"},
        {"name": "Inês Castelo"},
        {"name": "David Dias"},
        {"name": "Catarina Moura"},
        {"name": "Harshit Dhirajlal"},
        {"name": "Jacqueline Jardim"},
        {"name": "António Varela"},
        {"name": "João Dias"},
        {"name": "Bruno Gonçalves"},
        {"name": "Diogo Mónica"},
        {"name": "Vitor Canosa"},
        {"name": "Jorge Soares"},
        {"name": "Artur Assumpção"},
        {"name": "Nuno Melo"},
        {"name": "Jean Mousinho"},
        {"name": "João Vaz"},
        {"name": "Jorge Soares"},
        {"name": "Artur Assumpção"},
        {"name": "Marco Arede"},
        {"name": "Gonçalo Vicente"},
        {"name": "Diana Rodrigues"},
        {"name": "André geraldes"},
        {"name": "João Pacheco"},
        {"name": "Pedro Afonso"},
        {"name": "Fabio Domingos"},
        {"name": "Francisco Varandas"},
    ]
    for v in volunteers:
        try:
            socials = v.pop("socials", None)
            vo = Volunteer.objects.update_or_create(**v)[0]
            if socials:
                for social_name in socials:
                    sn = SocialNetwork.objects.update_or_create(name=social_name,
                                                                url=socials[social_name], is_from_branch=False)[0]
                    vo.socials.add(sn)
        except:
            pass


def init_projects():
    projects = [
        {"name": "IEEE Academic", "info": "This is IEEE Academic's gorgeous info.",
         "image": File(open(os.path.join(projects_folder, 'ieee_academic.png'), 'r')),
         "coordinator": [Volunteer.objects.get(ieee_contact="anisashahidian@ieee-ist.org")]},
        {"name": "EPICS", "info": "This is EPICS...", "image": "",
         "coordinator": [Volunteer.objects.get(ieee_contact="joanapalhinha@ieee-ist.org")]},
        {"name": "TV", "info": "We film this. And that.",
         "image": File(open(os.path.join(projects_folder, 'ieee_tv.png'), 'r')),
         "coordinator": [Volunteer.objects.get(ieee_contact="anisashahidian@ieee-ist.org")]},
        {"name": "TISP 2.0", "info": "Dedicated to promoting engineering in schools.",
         "image": File(open(os.path.join(projects_folder, 'tisp20.png'), 'r')),
         "coordinator": [Volunteer.objects.get(ieee_contact="pedrofreire@ieee-ist.org"),
                         Volunteer.objects.get(ieee_contact="diogobarradas@ieee-ist.org")]},
        {"name": "Motivational Weekends", "info": "We dont drink at this motivational weekends",
         "image": File(open(os.path.join(projects_folder, 'weekend.png'), 'r'))}
    ]

    relations = {
        "IEEE Academic": 'academic.md',
        "EPICS": 'epics.md',
        "TV": 'tv.md',
        "TISP 2.0": 'tisp.md',
        "Motivational Weekends": 'mw.md'
    }

    for p in projects:
        coordinators = p.pop("coordinator", [])
        pr = Projects.objects.update_or_create(**p)[0]
        pr.info = open(os.path.join(settings.BASE_DIR, 'markdowns', 'en', relations[pr.name])).read()
        pr.info_pt = open(os.path.join(settings.BASE_DIR, 'markdowns', 'pt', relations[pr.name])).read()
        for c in coordinators:
            pr.coordinator.add(c)
        pr.save()
        Tag.objects.create(name=pr.get_tagname())


def init_boards():
    teammembers = [

        {"team": Team.objects.create(begin_year=2016, end_year=2017),
         "members": [{"name": "Diogo Monteiro", "role": "Chair"},
                     {"name": "Inês Ferreira", "role": "Vice-Chair of Technical Activities"},
                     {"name": "Pedro Reganha", "role": "Vice-Chair of Student Activities"},
                     {"name": "Rui Santos", "role": "Secretary"},
                     {"name": "Bruno Machado", "role": "Treasurer"},
                     {"name": "Diogo Mesquita", "role": "CS Chair"},
                     {"name": "João Carvalho", "role": "EMBS Chair"},
                     {"name": "André Lopes", "role": "RAS Chair"},
                     {"name": "Rita Barreiros", "role": "WiE Chair"},
                     {"name": "André Pires", "role": "IAS Chair/Past Chair"},
                     {"name": "João Pedro Boavida", "role": "Counselor"}]
         },
        {"team": Team.objects.create(begin_year=2015, end_year=2016),
         "members": [{"name": "André Pires", "role": "Chair"},
                     {"name": "Joana Pereira", "role": "Vice-Chair of Technical Activities"},
                     {"name": "João Santos", "role": "Vice-Chair of Student Activities"},
                     {"name": "Ana Colaço", "role": "Secretary"},
                     {"name": "Sofia Ferreira", "role": "Treasurer"},
                     {"name": "Diogo Monteiro", "role": "CS Chair"},
                     {"name": "João Apura", "role": "EMBS Chair"},
                     {"name": "Rúben Capitão", "role": "RAS Chair"},
                     {"name": "Rita Barreiros", "role": "WiE Chair"},
                     {"name": "João Pedro Boavida", "role": "Counselor"}]
         },
        {"team": Team.objects.create(begin_year=2014, end_year=2015),
         "members": [{"name": "Sofia Ferreira", "role": "Chair"},
                     {"name": "João Santos", "role": "Vice-Chair of Technical Activities"},
                     {"name": "Diana Rodrigues", "role": "Vice-Chair of Student Activities"},
                     {"name": "André geraldes", "role": "Secretary"},
                     {"name": "João Pacheco", "role": "Treasurer"},
                     {"name": "Gonçalo Vicente", "role": "CS Chair"},
                     {"name": "Pedro Afonso", "role": "EMBS Chair"},
                     {"name": "Francisco Varandas", "role": "RAS Chair"},
                     {"name": "Anisa Shahidian", "role": "WiE Chair"},
                     {"name": "João Pedro Boavida", "role": "Counselor"}]
         },
        {"team": Team.objects.create(begin_year=2013, end_year=2014),
         "members": [{"name": "Catarina Martins", "role": "Chair"},
                     {"name": "Gonçalo Carito", "role": "Vice-Chair of Technical Activities"},
                     {"name": "Paula Monteiro", "role": "Vice-Chair of Student Activities"},
                     {"name": "Francisco Esteves", "role": "Secretary"},
                     {"name": "Diana Rodrigues", "role": "Treasurer"},
                     {"name": "Francisco Dias", "role": "CS Chair"},
                     {"name": "João Santos", "role": "RAS Chair"},
                     {"name": "Sofia Ferreira", "role": "WiE Chair"},
                     {"name": "Rui Rocha", "role": "Counselor"}]
         },
        {"team": Team.objects.create(begin_year=2012, end_year=2013),
         "members": [{"name": "Carmo Póvoa", "role": "Chair"},
                     {"name": "Rui Costa", "role": "Vice-Chair of Technical Activities"},
                     {"name": "Ricardo Câncio Silva", "role": "Vice-Chair of Student Activities"},
                     {"name": "Gonçalo Carito", "role": "Secretary"},
                     {"name": "Fábio Domingos", "role": "Treasurer"},
                     {"name": "João Azevedo", "role": "CS Chair"},
                     {"name": "Giovanna Franchi", "role": "IAS Chair"},
                     {"name": "Camille Coyac", "role": "WiE Chair"},
                     {"name": "Inês Fernandes", "role": "Membership Development"},
                     {"name": "Inês Castelo", "role": "Membership Development"},
                     {"name": "David Dias", "role": "Mentor"},
                     {"name": "Rui Rocha", "role": "Counselor"}]
         },
        {"team": Team.objects.create(begin_year=2011, end_year=2012),
         "members": [{"name": "David Dias", "role": "Chair"},
                     {"name": "Rui Costa", "role": "Vice-Chair of Technical Activities"},
                     {"name": "Fábio Domingos", "role": "Vice-Chair of Student Activities"},
                     {"name": "Carmo Póvoa", "role": "Secretary"},
                     {"name": "Camille Coyac", "role": "Treasurer"},
                     {"name": "Catarina Moura", "role": "WiE Chair"},
                     {"name": "Harshit Dhirajlal", "role": "Gold Liaison"},
                     {"name": "Jacqueline Jardim", "role": "Mentor"},
                     {"name": "António Varela", "role": "Counselor"}, ]
         },
        {"team": Team.objects.create(begin_year=2010, end_year=2011),
         "members": [{"name": "João Dias", "role": "Chair"},
                     {"name": "Jacqueline Jardim", "role": "Vice-Chair"},
                     {"name": "David Dias", "role": "Secretary"},
                     {"name": "Catarina Moura", "role": "Treasurer"},
                     {"name": "Harshit Dhirajlal", "role": "Liaison"},
                     {"name": "Fabio Domingos", "role": "Membership Activities Coordinator"},
                     {"name": "António Varela", "role": "Counselor"}, ]
         },
        {"team": Team.objects.create(begin_year=2009, end_year=2010),
         "members": [{"name": "Bruno Gonçalves", "role": "Chair"},
                     {"name": "Diogo Mónica", "role": "Vice-Chair"},
                     {"name": "Vitor Canosa", "role": "Treasurer/Secretary"}, ]
         },
        {"team": Team.objects.create(begin_year=2008, end_year=2009),
         "members": [{"name": "Jorge Soares", "role": "Chair"},
                     {"name": "Artur Assumpção", "role": "Vice-Chair"},
                     {"name": "Nuno Melo", "role": "Treasurer/Secretary"},
                     {"name": "Jean Mousinho", "role": "Alameda Campus Liaison"},
                     {"name": "Diogo Mónica", "role": "Taguspark Campus Liaison"},
                     {"name": "João Vaz", "role": "Counselor"}, ]
         },
        {"team": Team.objects.create(begin_year=2007, end_year=2008),
         "members": [{"name": "Jorge Soares", "role": "Chair"},
                     {"name": "Artur Assumpção", "role": "Vice-Chair"},
                     {"name": "Marco Arede", "role": "Treasurer/Secretary"},
                     {"name": "Jean Mousinho", "role": "Alameda Campus Liaison"},
                     {"name": "Diogo Mónica", "role": "Taguspark Campus Liaison"},
                     {"name": "João Vaz", "role": "Counselor"}, ]
         },
    ]

    for tm in teammembers:
        team = tm["team"]
        members = tm["members"]
        for member in members:
            v = Volunteer.objects.get(name=member['name'])
            TeamMember.objects.update_or_create(team=team, member=v, role=member['role'])


def init_social_networks():
    sns = [
        {'name': 'facebook', 'url': 'https://www.facebook.com/ieeeist/', 'is_from_branch': True},
        {'name': 'twitter', 'url': 'https://twitter.com/ieeeist', 'is_from_branch': True},
        {'name': 'instagram', 'url': 'https://www.instagram.com/ieee_ist/', 'is_from_branch': True},
    ]
    for sn in sns:
        SocialNetwork.objects.update_or_create(**sn)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            get_user_model().objects.create_superuser('administrator', 'admin@admin.com', 'tanque')
            u = get_user_model().objects.create_user('editor', 'editor@editor.com', 'ieeeist')
            g = Group.objects.get_or_create(name="Editors")
            u.groups.add(g)
            u.save()
        except:
            pass

        print "Loading volunteers..."
        init_volunteers()
        print "Done\nLoading Communities..."
        init_communities()
        print "Done\nLoading Projects..."
        init_projects()
        print "Done\nLoading Boards..."
        init_boards()
        print "Done\nLoading Socials..."
        init_social_networks()
        print "Done\n"
