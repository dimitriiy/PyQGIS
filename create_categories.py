import random

LAYER_NAME = 'POINT_LAYER'
layer = QgsProject.instance().mapLayersByName(LAYER_NAME)[0]
dlayer = layer.getFeatures()

def randColor():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    return QColor.fromRgb(a,b,c)

def groupFeatures(key):
    group_features = {}
    layer.select(selected_fid)
    for feature in dlayer:
        id = feature.id()
        zsp_id = feature[key]
        if zsp_id in  group_features:
            group_features[zsp_id].append(id)
        else:
            group_features[zsp_id] = [id]
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

    # Field name
    expression = groupBy
    # Set the categorized renderer
    renderer = QgsCategorizedSymbolRenderer(expression, categories)
    layer.setRenderer(renderer)
    # Refresh layer
    layer.triggerRepaint()


init('zsp_id')
