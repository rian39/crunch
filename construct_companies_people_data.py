import numpy as np
import pandas as pd
import json
import os
import graph_tool.all as gt

# load the companies data
company_files = os.listdir('data')
companies = {}  
for company in company_files:
    c = json.load(open('data/'+company))
    if c.has_key('permalink') :
        companies[c['permalink']] = c
    else:
        print(c)
print('Load %d company details' % len(companies))


#create table of companies and people
comp_people=[]
for name, company in companies.iteritems():
    for  rel in company['relationships']:
        person = rel['person']['permalink']
        comp_people.append((name, person))

comp_people_df = pd.DataFrame(comp_people, columns = ['company', 'person'])


#create table of companies and tag_list
comp_tag=[]
for name, company in companies.iteritems():
    if company.has_key('tag_list') and (company['tag_list'] is not None):
        tags = company['tag_list'].split(', ')
        for tag in tags:
            comp_tag.append((name, tag))

comp_tag_df = pd.DataFrame(comp_tag, columns = ['company', 'tag'])

#create dates of companies -- TBC
# [(name,'/'.join([company['founded_month'], company['founded_year']])) for name, company in companies.iteritems()]


comp_tag_table = pd.crosstab(comp_tag_df.company, comp_tag_df.tag)
m = comp_tag_table.as_matrix()

#can this matrix to project tags into each other; and companies into each other -- a way of connecting them

tag_tag = m.transpose().dot(m)
comp_comp = m.dot(m.transpose())

# create graph of connected
comp_comp_tri = np.tril(comp_comp)
g = gt.Graph( directed=False)

v = g.add_vertex(n=comp_comp_tri.shape[0])
v_company = g.new_vertex_property('string')
e_weight = g.new_edge_property("int")

company_count  = len(comp_comp_tri)

for i in range(0, company_count):
    v_company[v.next()] = comp_tag_table.index[i]

g.vertex_properties['company'] =  v_company

for i in range(0, len(comp_comp_tri)):
    for j in range (0, len(comp_comp_tri)):
        if i != j and comp_comp_tri [i,j] > 0:
            e = g.add_edge(g.vertex(i), g.vertex(j))
            e_weight[e] = comp_comp_tri[i,j]

g.edge_properties['weight'] = e_weight


# to filter the graph a bit
 v_bet, e_bet = gt.betweenness(g, weight=g.edge_properties['weight'])
 pos, it = gt.graph_draw(g, vertex_fill_color = v_bet, 
    vertex_size = gt.prop_to_size(v_bet, mi=2, ma=15),
    edge_pen_width = gt.prop_to_size(e_bet, mi=0.3, ma = 5))

# could use degree to filter

deg = g.degree_property_map(deg='total', weight = g.edge_properties['weight'])
companies_list = comp_tag_table.index
companies_list[deg.a.argmax()]
v_bet, e_bet = gt.betweenness(g, weight = g.edge_properties['weight'])
companies_list[v_bet.a.argmax()]
