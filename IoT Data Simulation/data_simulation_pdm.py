import json
import time
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker
from faker.providers import DynamicProvider


def pdm_simulator():
    print("Waiting for Data")
    fake = Faker()

    data_list = []

    for i in range(0, 1000):
        # ! Unique Identifier
        unique = random.randint(1, 1000)

        # ! Machine Type
        machine_provider = DynamicProvider(
            provider_name = "machine_type",
            elements = ["Low", "High", "Medium"])
        fake.add_provider(machine_provider)
        machine_type = fake.machine_type()

        # ! Machine ID
        if machine_type == "Low":
            product_id = random.randint(40000, 49999)
        elif machine_type == "Medium":
            product_id = random.randint(10000, 19999)
        else: 
            product_id = random.randint(20000, 29999)

        # ! Air Temperature
        air_temp = round(random.uniform(298.0, 305.0), 1)

        # ! Process Temperature
        process_temp = round(random.uniform(10.0, 10.6) + air_temp, 1)

        # ! Rotational Speed
        rotational_speed = random.randint(1160, 2860)

        # ! Torque
        torque = round(random.uniform(3.5, 66.5), 1)

        # ! Tool Wear (minutes)
        tool_wear = random.randint(0, 210)

        # ! Power
        power = rotational_speed * torque

        # ! Tool Wear Failure
        if(tool_wear > 200):
            twf = "Yes"
        else:
            twf = "No"

        # ! Heat Dissipation Failure
        if((process_temp - air_temp) < 10.1 and rotational_speed < 1380):
            hdf = "Yes"
        else:
            hdf = "No"
        
        # ! Power Failure
        unit_calc = round((rotational_speed * 0.1047198) * torque, 0)
        if(unit_calc < 2000.0 or unit_calc > 12000.0):
            pwf = "Yes"
        else:
            pwf = "No"

        # ! Overstrain Failure
        if(machine_type == "Low" and (tool_wear * torque) > 11000.0):
            osf = "Yes"
        elif(machine_type == "Medium" and (tool_wear * torque) > 12000.0):
            osf = "Yes"
        elif(machine_type == "High" and (tool_wear * torque) > 13000.0):
            osf = "Yes"
        else:
            osf = "No"

        # ! Random Failures
        rnf_provider = DynamicProvider(
            provider_name = "rnf",
            elements = ["Yes", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No",
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", 
                        "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No"])
        fake.add_provider(rnf_provider)
        rnf = fake.rnf()

        # ! Machine Failure
        if(twf == "Yes" or hdf == "Yes" or pwf == "Yes" or osf == "Yes" or rnf == "Yes"):
            mf = "Yes"
        else:
            mf = "No"

        data = {
            "UID": unique,
            "Machine ID": product_id,
            "Type": machine_type,
            "Air Temperature [K]": air_temp,
            "Process Temperature [K]": process_temp,
            "Rotational Speed [rpm]": rotational_speed,
            "Torque [Nm]": torque,
            "Tool Wear [mins]": tool_wear,
            "Power": power,
            "Tool Wear Failure": twf,
            "Heat Dissipation Failure": hdf,
            "Power Failure": pwf,
            "Overstrain Failure": osf,
            "Random Failure": rnf,
            "Machine Failure": mf
        }
        
        # ! Append to list
        data_list.append(data)
    
    df = pd.DataFrame.from_dict(data = data_list)
    df.to_csv("simulated_pdm_data.csv", index = False)

def main():
    pdm_simulator()

if __name__ == '__main__':
    main()
