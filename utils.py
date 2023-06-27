from sqlalchemy.orm import attributes


def sqlalchemy_obj_to_dict(obj):
    state = attributes.instance_state(obj)
    fields = state.mapper.mapped_table.columns.keys()
    data = {field: getattr(obj, field) for field in fields}
    return data


def room_dict_response(room, air_conditioners):
    room_dict = sqlalchemy_obj_to_dict(room)
    room_dict["air_conditioners"] = [
        sqlalchemy_obj_to_dict(air_conditioner) for air_conditioner in air_conditioners
    ]

    return room_dict
