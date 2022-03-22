import random

LAYER_NAME = 'POINT_LAYER'
layer = QgsProject.instance().mapLayersByName(LAYER_NAME)[0]
features = layer.getFeatures()

def randColor():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    return QColor.fromRgb(a,b,c)

def groupFeatures(attr):
    group_features = {}

    for feature in features:
        id = feature.id()
        group_by_key = feature[attr]
        if group_by_key in  group_features:
            group_features[group_by_key].append(id)
        else:
            group_features[group_by_key] = [id]
    return group_features


def init(groupBy):
    grouped_features = groupFeatures(groupBy)
    land_class = {}
        
    for key in grouped_features.keys():
        land_class[key] = [randColor(),key]
        
    categories = []
    # Iterate through the dictionary
    for classes, (color, label) in land_class.items():
        print(str(label),classes)
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(color)
        category = QgsRendererCategory(classes, symbol, str(label))
        categories.append(category)

    expression = groupBy
    renderer = QgsCategorizedSymbolRenderer(expression, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


init('zsp_id')
