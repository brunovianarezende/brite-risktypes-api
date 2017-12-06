from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, asc

from brite.model import RiskType, AttributeDataType, AttributeTypeDate,\
    AttributeTypeEnum, AttributeTypeEnumValue, AttributeTypeInt, AttributeTypeNumeric,\
    AttributeTypeText

_STR2ENUM = {
    'date': AttributeDataType.DATE,
    'enum': AttributeDataType.ENUM,
    'text': AttributeDataType.TEXT,
    'numeric': AttributeDataType.NUMERIC,
    'int': AttributeDataType.INT,
}

_ENUM2STR = {
    v: k for k, v in _STR2ENUM.items()
}

def str2enum(s):
    return _STR2ENUM[s]

def enum2str(e):
    return _ENUM2STR[e]

def _data_type2model_type(dt):
    return {
        AttributeDataType.DATE: AttributeTypeDate,
        AttributeDataType.ENUM: AttributeTypeEnum,
        AttributeDataType.INT: AttributeTypeInt,
        AttributeDataType.NUMERIC: AttributeTypeNumeric,
        AttributeDataType.TEXT: AttributeTypeText,
    }[dt]

def _set_if_not_none(d, key, value):
    if value is not None:
        d[key] = value

class DbService:
    def __init__(self, engine):
        self._engine = engine
        self._Session = sessionmaker(bind=engine)

    def add_type(self, type_description):
        session = self._Session()
        risk_type = RiskType(name=type_description['name'], description=type_description['description'])
        session.add(risk_type)

        for attribute in type_description.get('attributes', []):
            args = {
                'name': attribute['name'],
                'description': attribute.get('description'),
                'data_type': str2enum(attribute['type'])
            }
            
            if args['data_type'] == AttributeDataType.ENUM:
                args['allowed_values'] = [
                    AttributeTypeEnumValue(value=v) for v in attribute.get('allowed_values', [])
                ]
            model_type = _data_type2model_type(args['data_type'])
            attribute_type = model_type(**args)
            risk_type.attributes.append(attribute_type)

        session.commit()
        return risk_type.id

    def get_type(self, type_id):
        session = self._Session()
        risk_type = session.query(RiskType).filter_by(id=type_id).first()
        return None if risk_type is None else self._model_type2service_type(risk_type)

    def _model_type2service_type(self, model_type):
        result = {
            'id': model_type.id,
            'name': model_type.name,
            'attributes': [],
        }
        _set_if_not_none(result, 'description', model_type.description)

        for attribute_type in model_type.attributes:
            attribute = {
                'id': attribute_type.id,
                'name': attribute_type.name,
                'type': enum2str(attribute_type.data_type)
            }
            _set_if_not_none(attribute, 'description', attribute_type.description)
            if attribute_type.data_type == AttributeDataType.ENUM:
                attribute['allowed_values'] = [v.value for v in attribute_type.allowed_values]
            result['attributes'].append(attribute)

        return result

    def get_types(self, order_by_name=False):
        session = self._Session()
        query = session.query(RiskType)
        if order_by_name:
            query = query.order_by(func.lower(RiskType.name))
        risk_types = query.all()
        return [self._model_type2service_type(r) for r in risk_types]
