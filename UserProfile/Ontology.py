from UserProfile.CosineCalculator import CosineSimilarity
from owlready2 import *

scriptpath = os.path.dirname(__file__)
onto = get_ontology("file://"+ scriptpath + "//User_Ontology.owl").load()
my_world = World()
my_world.get_ontology("file://"+ scriptpath + "//User_Ontology.owl").load()
sync_reasoner(my_world)
graph = my_world.as_rdflib_graph()

class OntologyModule:
    def checkCategory(ins):
        resultsList = graph.query("base <http://www.semanticweb.org/jithmiweerasekara/ontologies/User_Ontology> "
                                  "SELECT ?cat "
                                  "WHERE { "
                                  "<#" + ins + "> a ?cat . "
                                               "}")
        # creating json object
        response = []
        for item in resultsList:
            result = str(item['cat'].toPython())
            result = re.sub(r'.*#', "", result)
            response.append({'cat': result})

        return result

    def food_ontology(tweet):
        preference= []
        for j in onto.FoodPreference.instances():
            # duplicates = False
            ins1 = re.sub('User_Ontology.', '', str(j))
            score_food = CosineSimilarity.calculateCosinesimilarity(tweet, ins1)
            if (score_food > 0.0):
                food_preference = OntologyModule.checkCategory(ins1)
                preference.append(food_preference)
        return preference

    def env_ontology(tweet):
        preference = []
        for j in onto.EnvironmentPreference.instances():
            # duplicates = False
            ins1 = re.sub('User_Ontology.', '', str(j))
            score_env = CosineSimilarity.calculateCosinesimilarity(tweet, ins1)
            if (score_env > 0.0):
                env_preference = OntologyModule.checkCategory(ins1)
                preference.append(env_preference)
        return preference

    def eco_ontology(tweet):
        preference = []
        for j in onto.EconomyLevel.instances():
            ins1 = re.sub('User_Ontology.', '', str(j))
            score_eco = CosineSimilarity.calculateCosinesimilarity(tweet, ins1)
            if (score_eco > 0.0):
                eco_level = OntologyModule.checkCategory(ins1)
                preference.append(eco_level)
        return preference