test_files = [
    "../input_data/a_an_example.in.txt",
    "../input_data/b_better_start_small.in.txt",
    "../input_data/c_collaboration.in.txt",
    "../input_data/d_dense_schedule.in.txt",
    "../input_data/e_exceptional_skills.in.txt",
    "../input_data/f_find_great_mentors.in.txt"
]

def parse_problem(lines):
    [cont_num, proj_num] = [int(n) for n in lines[0].split(" ")]
    contributor_ds = {}
    project_ds = {}

    curr_line = 1
    for cnum in range(cont_num):
        contrib_header = lines[curr_line]

        [contrib_name, num_skills] = contrib_header.split(" ")
        contributor_ds[contrib_name] = {}
        num_skills = int(num_skills)

        skills_lines = lines[curr_line + 1: curr_line + 1 + num_skills]

        for skill_line in skills_lines:
            skill_name, level = skill_line.split(" ")
            level = int(level)
            contributor_ds[contrib_name][skill_name] = level

        curr_line += 1 + num_skills

    for pnum in range(proj_num):
        proj_header = lines[curr_line]
        proj_name, days, score, best_before, num_roles = proj_header.split(" ")
        num_roles = int(num_roles)
        project_ds[proj_name] = {
            "days": int(days),
            "score": int(score),
            "best_before": int(best_before),
            "roles": {},
            "roles_order": [],
            # "roles": [],
        }

        roles_lines = lines[curr_line + 1: curr_line + 1 + num_roles]

        for role_line in roles_lines:
            role_name, level = role_line.split(" ")
            level = int(level)
            project_ds[proj_name]["roles_order"].append((role_name, level))
            if role_name not in project_ds[proj_name]["roles"]:
                project_ds[proj_name]["roles"][role_name] = []
            project_ds[proj_name]["roles"][role_name].append(level)
            # role_ds = {}
            # role_ds[role_name] = level
            # project_ds[proj_name]["roles"].append(role_ds)

        curr_line += 1 + num_roles

    return contributor_ds, project_ds


def parse_file(f_path):
    with open(f_path) as t:
        text = t.read()
        lines = text.split('\n')
        return parse_problem(lines)


def has_skill(contributor_ds, name, skill) -> bool:
    return name in contributor_ds and skill in contributor_ds[name]


def assignment_dic_and_order_to_output(a_dic, a_ord):
    lines = []
    num_proj = len(a_ord)
    lines.append(str(num_proj))
    for proj in a_ord:
        lines.append(proj)
        lines.append(" ".join(a_dic[proj]))
    return "\n".join(lines)

def proj_profit_key_with_roles(proj_dict, proj):
  return proj_dict[proj]["score"] /proj_dict[proj]["days"] / len(proj_dict[proj]["roles_order"])

def ordered_by_profit_ratio_with_roles(input_path):
    from copy import deepcopy
    cont, proj_dict = parse_file(input_path)

    assigned_proj = {}
    assigned_order = []

    # next_free_day = {}
    # for c_name in cont.keys():
    #   next_free_day[c_name] = 0

    # curr_day = 0

    sorted_proj = list(proj_dict.keys())
    sorted_proj.sort(key=lambda proj: proj_profit_key_with_roles(proj_dict, proj))
    sorted_proj.reverse()

    for proj in sorted_proj:
        # if proj in assigned_proj:
        #   continue
        settings = proj_dict[proj]
        assigned_roles = {}
        assigned_contrib = []

        remaining_roles = deepcopy(settings['roles'])
        for c_name, c_roles in cont.items():
            if c_name in assigned_contrib:
                continue

            # print(c_name, c_roles)
            for role, c_level in c_roles.items():
                if c_name in assigned_contrib:
                    break

                if role in remaining_roles:
                    for req_idx, req_level in enumerate(remaining_roles[role]):
                        if c_level >= req_level:
                            if (role, req_level) not in assigned_roles:
                                assigned_roles[(role, req_level)] = []

                            assigned_roles[(role, req_level)].append(c_name)
                            assigned_contrib.append(c_name)
                            remaining_roles[role].pop(req_idx)
                            if len(remaining_roles[role]) == 0:
                                del remaining_roles[role]
                            break


                if len(remaining_roles.keys()) == 0:
                    break

            if len(remaining_roles.keys()) == 0:
                break

        if len(remaining_roles.keys()) == 0:
            ordered_roles = []
            for role_key in settings['roles_order']:
                ordered_roles.append(assigned_roles[role_key].pop(0))
            assigned_proj[proj] = ordered_roles
            assigned_order.append(proj)
            continue

        # print("failed to assign", proj, remaining_roles)

    # print("assigned proj", assigned_proj)
    return assigned_proj, assigned_order

out_names = ["a", "b", "c", "d", "e", "f"]
results = []

for tf in test_files:
    a_dic, a_ord = ordered_by_profit_ratio_with_roles(tf)
    results.append(assignment_dic_and_order_to_output(a_dic, a_ord))

for idx, res in enumerate(results):
    with open(f"./{out_names[idx]}.txt", "w") as f:
        f.write(res)
