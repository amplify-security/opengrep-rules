#!/usr/bin/env python3
import os
import json
import yaml

def load_configs():
    directory = 'configs'
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".list"):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    data.append(tuple(line.strip().split(':')))
    print(f'I:loaded {len(data)} rules from configs, removing {len(data) - len(set(data))} duplicates')
    # There is some rule overlap in our configuration lists, so this dedups the list
    return set(data)

def collect_rules(rule_list):
    accumulated_rules = []
    for item in rule_list:
        rules_file, rule_id = item
        rule_prefix = rules_file.replace('/', '.').replace('.yaml', '')
        if os.path.isfile(rules_file):
            with open(rules_file, 'r') as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                if 'rules' in yaml_data:
                    rule_found = False
                    for rule in yaml_data['rules']:
                        if rule.get('id') == rule_id:
                            rule['id'] = f'{rule_prefix}.{rule_id}'
                            accumulated_rules.append(rule)
                            rule_found = True
                    if not rule_found:
                        print(f'W:rule {rule_id} not found in {rules_file}')
                else:
                    print(f'E:unable to load rule {rule_id} as {rules_file} does not appear to contain rules')
        else:
            print(f'W:skipping {item} as {rules_file} does not exist')

    return accumulated_rules

def main():
    rule_list = load_configs()
    rules = collect_rules(rule_list)
    print(f'I:collected {len(rules)} rules')

    with open('rules.json', 'w') as json_file:
        json.dump({'rules': rules}, json_file)
        print('I:rules written to rules.json')

if __name__ == "__main__":
    main()
