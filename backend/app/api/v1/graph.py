"""OpsPilot — Knowledge Graph Routes"""

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("/explore", summary="Explore knowledge graph")
async def explore_graph(user_id: str = Depends(get_current_user_id)):
    try:
        from app.db.neo4j_client import neo4j_client
        if not neo4j_client.driver:
            return {"nodes": [], "edges": []}
            
        cypher = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, labels(n) as n_labels, elementId(n) as n_id, r, type(r) as r_type, m, labels(m) as m_labels, elementId(m) as m_id
        LIMIT 500
        """
        records = await neo4j_client.execute_query(cypher)
        
        nodes_dict = {}
        edges = []
        
        for record in records:
            n = record.get("n")
            n_labels = record.get("n_labels", [])
            n_id = record.get("n_id")
            if n is not None and n_id is not None:
                node_id = n.get("id") or n_id
                nodes_dict[node_id] = {
                    "id": node_id,
                    "label": n_labels[0] if n_labels else "Node",
                    "properties": n
                }
                
            r = record.get("r")
            r_type = record.get("r_type")
            m = record.get("m")
            m_labels = record.get("m_labels", [])
            m_id = record.get("m_id")
            if r is not None and m is not None and m_id is not None:
                target_id = m.get("id") or m_id
                nodes_dict[target_id] = {
                    "id": target_id,
                    "label": m_labels[0] if m_labels else "Node",
                    "properties": m
                }
                
                # handle if r is a tuple or dict
                if isinstance(r, tuple):
                    r_props = r[0] if len(r) > 0 else {}
                else:
                    r_props = r
                    
                edges.append({
                    "id": f"{node_id}-{r_type}-{target_id}",
                    "source": node_id,
                    "target": target_id,
                    "type": r_type or "RELATED_TO",
                    "properties": r_props
                })
                
        # Deduplicate edges just in case
        unique_edges = []
        seen_edges = set()
        for e in edges:
            sig = f"{e['source']}-{e['type']}-{e['target']}"
            if sig not in seen_edges:
                seen_edges.add(sig)
                unique_edges.append(e)

        return {
            "nodes": list(nodes_dict.values()),
            "edges": unique_edges
        }
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Graph explore failed: {e}")
        return {"nodes": [], "edges": []}


@router.get("/node/{node_id}", summary="Get node detail")
async def get_node(node_id: str, user_id: str = Depends(get_current_user_id)):
    return {"message": "Not implemented"}


@router.get("/search", summary="Search graph")
async def search_graph(query: str = "", user_id: str = Depends(get_current_user_id)):
    return {"nodes": [], "edges": []}


@router.get("/path", summary="Find shortest path")
async def find_path(
    source_id: str = "",
    target_id: str = "",
    user_id: str = Depends(get_current_user_id),
):
    return {"path": []}
