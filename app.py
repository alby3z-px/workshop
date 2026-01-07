import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import csv
import hashlib

DATA_DIR = Path("data")
AGGREGATED_FILE = DATA_DIR / "aggregated.json"
UPLOADS_DIR = Path("uploads")
PRODUCT_CATALOG_FILE = UPLOADS_DIR / "Product Catalog 2c34aca9ecb38075ab7fcdbec29ce503.csv"

st.set_page_config(page_title="Workshop Session Capture", layout="wide")

# --- Helpers ---

def get_owner_color(owner_name: str) -> str:
    """Generate a consistent color for a business owner based on their name."""
    colors = ['#1976d2', '#d32f2f', '#388e3c', '#f57c00', '#7b1fa2', '#00796b', '#5e35b1', '#c62828']
    # Hash the owner name to get a consistent index
    hash_val = int(hashlib.md5(owner_name.encode()).hexdigest(), 16)
    return colors[hash_val % len(colors)]


def ensure_dirs():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    AGGREGATED_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not AGGREGATED_FILE.exists():
        with open(AGGREGATED_FILE, "w") as f:
            json.dump({"products": {}, "business_owners": {}}, f)


def slugify(name: str) -> str:
    s = name.lower().strip()
    # keep alnum, dash
    import re
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip('-')


def get_empty_product_template():
    """Return a template with all product fields initialized."""
    return {
        # Core metadata
        "product_id": "",
        "product_name": "",
        "workstream": "",
        "business_owner": "",
        "existing_users": "",
        "primary_operator": "",
        "primary_developer": "",
        
        # Technical session structure
        "technical_session": {
            "part1_overview": {
                "overview_product_desc": "",
                "overview_problem_solved": "",
                "overview_process_fit": "",
                "overview_history": "",
                "overview_alignment": ""
            },
            "part2_technical_stack": {
                "tech_languages_versions": "",
                "tech_frameworks_libs": "",
                "tech_commercial_tools": "",
                "tech_dependencies_external": "",
                "tech_dependencies_internal": "",
                "tech_runtime_env": "",
                "tech_os_requirements": "",
                "tech_hardware_needs": ""
            },
            "part3_development_deployment": {
                "dev_feature_request": "",
                "dev_roadmap": "",
                "dev_version_control": "",
                "dev_code_reviews": "",
                "dev_testing": "",
                "dev_docs": "",
                "dev_deploy_process": "",
                "dev_deploy_roles": "",
                "dev_deploy_duration": "",
                "dev_operator_coordination": "",
                "dev_operator_comms": ""
            },
            "part4_challenges": {
                "challenges_limitations": "",
                "challenges_rewrite": "",
                "challenges_tech_debt": "",
                "challenges_maintainability": "",
                "challenges_docs_training": ""
            },
            "part5_operation_deepdive": {
                "usage_access": {
                    "usage_frequency": "",
                    "usage_tasks": "",
                    "usage_duration": "",
                    "access_method": "",
                    "access_permissions": "",
                    "access_locations": "",
                    "training_type": "",
                    "training_duration": "",
                    "training_docs": ""
                },
                "pain_points_workarounds": {
                    "ops_pain_points": "",
                    "ops_slowdowns": "",
                    "ops_workarounds": "",
                    "ops_failure_detection": "",
                    "ops_self_debug": "",
                    "ops_support_contact": "",
                    "ops_resolution_time": "",
                    "ops_missing_features": ""
                },
                "gap_analysis": {
                    "gap_output_quality": "",
                    "gap_timeline_speed": "",
                    "gap_unavailability": "",
                    "gap_alternatives": ""
                }
            },
            "part6_data_integration": {
                "data_inputs": {
                    "data_inputs_sources": "",
                    "data_inputs_format": "",
                    "data_inputs_frequency": "",
                    "data_inputs_ingestion": "",
                    "data_inputs_time": "",
                    "data_inputs_prep": "",
                    "data_inputs_failure": "",
                    "data_inputs_volume": "",
                    "data_inputs_growth": "",
                    "data_inputs_retention": ""
                },
                "data_outputs": {
                    "data_outputs_types": "",
                    "data_outputs_destinations": "",
                    "data_outputs_format": "",
                    "data_outputs_export": "",
                    "data_outputs_post": "",
                    "data_outputs_retention": ""
                },
                "data_storage": {
                    "data_storage_locations": "",
                    "data_storage_access": "",
                    "data_storage_backup": "",
                    "data_storage_recovery": ""
                },
                "integration_points": {
                    "integrations_nuton": "",
                    "integrations_external": "",
                    "integrations_desired": ""
                }
            },
            "part7_wrapup": {
                "maturity_scores": {
                    "maturity_development": 3,
                    "maturity_operational": 3,
                    "maturity_data": 3,
                    "maturity_integration": 3,
                    "maturity_documentation": 3
                },
                "prioritization_improvement": "",
                "critical_unknowns": "",
                "predict_platform_fit": "",
                "summary_validation": "",
                "quotes": []
            }
        },
        
        # Simplified fields for basic edit form
        "simple_edit": {
            "date": "",
            "duration_minutes": 90,
            "attendees": [],
            "recording_link": "",
            "technical_stack": "",
            "dev_practices": "",
            "top_pain_points": ""
        },
        
        # No timestamps persisted
    }


def get_empty_business_owner_template():
    """Return a template with all business owner fields initialized."""
    return {
        "owner_name": "",
        "products_covered": [],
        
        "part1_context_business_process": {
            "context_role": "",
            "context_stages": "",
            "context_decisions": "",
            "context_deliverables": "",
            "context_workflow": "",
            "context_steps": "",
            "context_info_needed": "",
            "context_decision_points": "",
            "context_partner_impact": "",
            "context_partner_confidence": "",
            "context_partner_frustration": ""
        },
        
        "part2_product_portfolio_review": {
            "section_a_business_owner": {
                "product_purpose": "",
                "product_why_created": "",
                "product_what_achieve": "",
                "product_impact_works_well": "",
                "product_impact_doesnt_work": "",
                "product_time_impact": "",
                "product_quality_decisions": "",
                "product_partner_confidence": ""
            },
            "section_b_users": {
                "b1_use_overview": {
                    "use_purpose": "",
                    "use_frequency": "",
                    "use_who_else": "",
                    "use_workflow_stage": "",
                    "use_critical_path": "",
                    "use_decisions": "",
                    "use_decision_explanation": "",
                    "use_critical_decisions": "",
                    "use_confidence_outputs": "",
                    "use_decisions_without_product": "",
                    "use_why_not_direct": ""
                },
                "b2_pain_points_gaps": {
                    "pain_frustrations": "",
                    "pain_slowdowns": "",
                    "pain_extra_work": "",
                    "pain_rework_errors": "",
                    "pain_unsupported_needs": "",
                    "pain_content_quality": "",
                    "pain_timeline": "",
                    "pain_usability": "",
                    "pain_missing_info": "",
                    "pain_missing_decisions": "",
                    "pain_manual_work": "",
                    "pain_workarounds": "",
                    "pain_time_added": "",
                    "pain_why_necessary": ""
                }
            }
        },
        
        "part3_cross_product_process": {
            "section_a_integration": {
                "integration_products_work_together": "",
                "integration_manual_data_movement": "",
                "integration_gaps": "",
                "integration_combine_info": "",
                "integration_how_combine": "",
                "integration_time_to_combine": "",
                "integration_error_prone": "",
                "integration_outside_products": "",
                "integration_outside_fit": ""
            },
            "section_b_bottlenecks": {
                "bottleneck_where_slows": "",
                "bottleneck_waiting_info": "",
                "bottleneck_manual_steps": "",
                "bottleneck_rework": "",
                "bottleneck_handoffs": "",
                "bottleneck_takes_longer": "",
                "bottleneck_why_long": "",
                "bottleneck_faster_look_like": "",
                "bottleneck_partner_delays": "",
                "bottleneck_partner_waiting": "",
                "bottleneck_partner_frustrations": ""
            }
        },
        
        "part4_partner_delivery": {
            "section_a_info_needs": {
                "partner_info_needs": "",
                "partner_info_frequency": "",
                "partner_info_format": "",
                "partner_delivery_method": "",
                "partner_delivery_time": "",
                "partner_delivery_automated": "",
                "partner_value_cant_provide": ""
            },
            "section_b_confidence_trust": {
                "partner_confidence_builders": "",
                "partner_concerns": "",
                "partner_demonstrate_data_led": ""
            }
        },
        
        "part5_ideal_future_state": {
            "section_a_prioritization": {
                "priority_biggest_impact": "",
                "priority_why": "",
                "priority_impact_detail": "",
                "priority_frequency": "",
                "priority_prevents_faster": "",
                "priority_partner_difference": ""
            },
            "section_b_vision": {
                "vision_day_to_day": "",
                "vision_can_do_new": "",
                "vision_decisions_faster": "",
                "vision_partner_delivery_changed": "",
                "vision_information_access": "",
                "vision_questions_answer": "",
                "vision_answer_speed": "",
                "vision_information_confidence": "",
                "vision_workflow_changed": "",
                "vision_manual_steps_gone": "",
                "vision_whats_faster": "",
                "vision_whats_easier": "",
                "vision_whats_reliable": "",
                "vision_partner_experience_faster": "",
                "vision_partner_confidence": "",
                "vision_partner_access": ""
            },
            "section_c_capabilities": {
                "capability_requirements": "",
                "capability_fast_enough": "",
                "capability_quality_requirements": ""
            }
        },
        
        "part6_wrapup": {
            "summary_validation": "",
            "summary_missed": "",
            "summary_most_important": "",
            "summary_critical_not_discussed": "",
            "summary_ensure_understanding": ""
        },
        
        
    }


def deep_merge(target, source):
    """Deep merge source dict into target dict."""
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


def save_product_data(product_id, product_data):
    """Save or update product data directly in aggregated.json."""
    aggregated = load_aggregated_data()
    
    if product_id not in aggregated["products"]:
        # Initialize with full template
        aggregated["products"][product_id] = get_empty_product_template()
    
    # Deep merge to preserve nested structures
    deep_merge(aggregated["products"][product_id], product_data)
    
    save_aggregated_data(aggregated)


def save_business_owner_data(owner_name, owner_data):
    """Save or update business owner data directly in aggregated.json."""
    aggregated = load_aggregated_data()
    
    if owner_name not in aggregated["business_owners"]:
        # Initialize with full template
        aggregated["business_owners"][owner_name] = get_empty_business_owner_template()
    
    # Update all fields from owner_data
    aggregated["business_owners"][owner_name].update(owner_data)
    
    save_aggregated_data(aggregated)


def load_products():
    """Load products from aggregated data."""
    aggregated = load_aggregated_data()
    products = []
    
    for pid, prod_data in aggregated.get("products", {}).items():
        product = dict(prod_data)  # Copy all fields directly
        products.append(product)
    
    return products


def migrate_remove_last_updated():
    """Remove deprecated 'last_updated' fields from aggregated.json if present."""
    data = load_aggregated_data()
    changed = False
    # Clean products
    for pid, prod in list(data.get("products", {}).items()):
        if isinstance(prod, dict) and "last_updated" in prod:
            del prod["last_updated"]
            changed = True
    # Clean business owners
    for owner, bo in list(data.get("business_owners", {}).items()):
        if isinstance(bo, dict) and "last_updated" in bo:
            del bo["last_updated"]
            changed = True
    if changed:
        save_aggregated_data(data)


def load_products_from_csv():
    """Parse Product Catalog CSV and extract products with all relevant metadata."""
    products_list = []
    if not PRODUCT_CATALOG_FILE.exists():
        return products_list
    
    try:
        with open(PRODUCT_CATALOG_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Skip header row
        for i, row in enumerate(rows):
            if i == 0:
                continue  # Skip header
            
            if not row or all(c.strip() == '' for c in row):
                continue
            
            product_name = row[0].strip() if len(row) > 0 else ''
            
            # Skip platform rows (no actual product name)
            if not product_name or 'Platform' in product_name and 'N/A' in (row[2] if len(row) > 2 else ''):
                continue
            
            # Extract only the fields used in UI
            workstream = row[1].strip() if len(row) > 1 else ''
            business_owner = row[3].strip() if len(row) > 3 else ''
            existing_users = row[4].strip() if len(row) > 4 else ''
            primary_operator = row[6].strip() if len(row) > 6 else ''
            primary_developer = row[10].strip() if len(row) > 10 else ''
            
            products_list.append({
                'product_name': product_name,
                'workstream': workstream,
                'business_owner': business_owner,
                'existing_users': existing_users,
                'primary_operator': primary_operator,
                'primary_developer': primary_developer
            })
    except Exception:
        pass
    
    return products_list



def load_aggregated_data():
    """Load aggregated data (products and business owners)."""
    if AGGREGATED_FILE.exists():
        with open(AGGREGATED_FILE, 'r') as f:
            return json.load(f)
    return {"products": {}, "business_owners": {}}


def save_aggregated_data(data):
    """Save aggregated data to file."""
    with open(AGGREGATED_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def import_products_from_csv():
    """Import products from CSV into aggregated.json."""
    aggregated = load_aggregated_data()
    csv_products = load_products_from_csv()
    
    # Track business owners for template pre-population
    business_owners = set()
    
    for csv_prod in csv_products:
        pid = slugify(csv_prod['product_name'])
        # Only add if not already exists
        if pid not in aggregated["products"]:
            # Start with full template
            new_product = get_empty_product_template()
            # Update with CSV data
            new_product.update(csv_prod)
            new_product["product_id"] = pid
            aggregated["products"][pid] = new_product
        
        # Track business owner
        owner = csv_prod.get('business_owner', '')
        if owner:
            business_owners.add(owner)
    
    # Pre-populate business owner templates with their products
    for owner in business_owners:
        if owner not in aggregated["business_owners"]:
            aggregated["business_owners"][owner] = get_empty_business_owner_template()
        
        # Always update products_covered list to keep it in sync
        products_for_owner = [p for p in aggregated["products"].values() 
                             if p.get('business_owner') == owner]
        aggregated["business_owners"][owner]['products_covered'] = [
            p['product_name'] for p in products_for_owner
        ]
    
    save_aggregated_data(aggregated)
    return aggregated


def get_product_data(product_id):
    """Get product data from aggregated.json."""
    aggregated = load_aggregated_data()
    return aggregated.get("products", {}).get(product_id, {})


def get_business_owner_data(owner_name):
    """Get business owner data from aggregated.json."""
    aggregated = load_aggregated_data()
    return aggregated.get("business_owners", {}).get(owner_name, {})


# --- UI ---

def main():
    ensure_dirs()
    # Migrate existing data to remove deprecated fields
    migrate_remove_last_updated()

    st.title("Workshop Product Page Editor")
    st.sidebar.header("Navigation")
    # Navigation buttons
    nav = {
        'Products': st.sidebar.button('Products', key='nav_products'),
        'Business Owner Sessions': st.sidebar.button('Business Owner Sessions', key='nav_business_sessions'),
        'Export Backup': st.sidebar.button('Export Backup', key='nav_export'),
    }
    
    # Import products from CSV
    st.sidebar.markdown("---")
    if st.sidebar.button('Import from CSV', key='import_csv'):
        import_products_from_csv()
        st.sidebar.success("✅ Products imported from CSV")
        st.rerun()
    
    # Determine current page
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Products'
    for k, v in nav.items():
        if v:
            st.session_state['page'] = k
    page = st.session_state['page']    
    # Highlight active page in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Current: {page}**")
    if page == 'Add Product':
        st.subheader("Add New Product")
        with st.form("add_product_form"):
            product_name = st.text_input("Product name (ID)")
            workstream = st.text_input("Workstream")
            business_owner = st.text_input("Business Owner")
            users = st.text_area("User(s)", height=40)
            primary_operator = st.text_input("Primary Operator")
            primary_developer = st.text_input("Primary Developer")
            primary_business_need = st.text_area("Primary Business Need", height=40)
            submitted = st.form_submit_button("Add product")
            if submitted:
                pid = slugify(product_name)
                product_data = {
                    'product_id': pid,
                    'product_name': product_name,
                    'workstream': workstream,
                    'business_owner': business_owner,
                    'existing_users': users,
                    'primary_operator': primary_operator,
                    'primary_developer': primary_developer,
                    'primary_business_need': primary_business_need,
                }
                save_product_data(pid, product_data)
                st.success("Product added ✅")
                st.session_state['editing_product'] = pid
                st.session_state['selected_product'] = pid
                st.session_state['page'] = 'Product Operator/Developer Session'
                st.rerun()

    elif page == 'Products':
        col1, col2 = st.columns([6, 1])
        with col1:
            st.header("Products")
        with col2:
            if st.button("➕ Add Product", key="add_product_btn"):
                st.session_state['page'] = 'Add Product'
                st.rerun()
        
        products = load_products()
        if not products:
            st.info("No products found yet. Click 'Add Product' to create one.")
        else:
            valid_products = [p for p in products if p.get('product_id') and p.get('product_name')]
            if not valid_products:
                st.info("No products found yet. Use 'Add Product' to create one.")
            else:
                # Column headers
                header_cols = st.columns([4, 3, 1, 1])
                header_cols[0].write("**Product Name**")
                header_cols[1].write("**Business Owner**")
                header_cols[2].write("")
                header_cols[3].write("")
                
                for p in valid_products:
                    owner = p.get('business_owner', 'Unknown')
                    bg_color = get_owner_color(owner)
                    
                    # Create row with background color on business owner cell
                    cols = st.columns([4, 3, 1, 1])
                    cols[0].write(p.get("product_name"))
                    cols[1].markdown(f'<div style="background-color: {bg_color}; color: white; padding: 8px; border-radius: 5px;">{owner}</div>', unsafe_allow_html=True)
                    if cols[2].button("Edit", key=f"edit-{p.get('product_id')}"):
                        st.session_state['editing_product'] = p.get('product_id')
                        st.session_state['page'] = 'Product Operator/Developer Session'
                        st.rerun()
                    if cols[3].button("Delete", key=f"delete-{p.get('product_id')}"):
                        st.session_state['delete_product_id'] = p.get('product_id')
                        st.session_state['show_delete_confirm'] = True
                        st.rerun()

            # Confirmation dialog for delete
            delete_pid = st.session_state.get('delete_product_id')
            if st.session_state.get('show_delete_confirm') and delete_pid:
                st.warning(f"Are you sure you want to delete product '{delete_pid}' and all its associated data? This cannot be undone.")
                confirm, cancel = st.columns(2)
                if confirm.button("Confirm Delete", key="confirm-delete"):
                    # Remove product from aggregated data
                    aggregated = load_aggregated_data()
                    if delete_pid in aggregated.get("products", {}):
                        del aggregated["products"][delete_pid]
                    save_aggregated_data(aggregated)
                    st.success(f"Product '{delete_pid}' deleted.")
                    st.session_state['delete_product_id'] = None
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()
                if cancel.button("Cancel", key="cancel-delete"):
                    st.session_state['delete_product_id'] = None
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

    elif page == 'Product Operator/Developer Session':
        editing_pid = st.session_state.get('editing_product')
        if not editing_pid:
            st.warning("No product selected for editing. Please select a product from the Products page.")
            if st.button("Go to Products"):
                st.session_state['page'] = 'Products'
                st.rerun()
            return
        products = load_products()
        product_data = get_product_data(editing_pid)
        
        # Get product info from the products list (has CSV data)
        product_info = next((p for p in products if p.get('product_id') == editing_pid), None)
        
        if not product_data and not product_info:
            st.error("Selected product not found. Please select another product.")
            if st.button("Go to Products"):
                st.session_state['page'] = 'Products'
                st.session_state['editing_product'] = None
                st.rerun()
            return
        
        # Merge info from both sources
        display_info = {}
        if product_info:
            display_info = dict(product_info)
        if product_data:
            display_info.update({k: v for k, v in product_data.items() if v})
        
        st.subheader("Operator/Developer Session")
        st.markdown(f"### {display_info.get('product_name', editing_pid)}")
        
        # Product Information - Always visible at top
        with st.expander("📝 Product Information", expanded=True):
            with st.form(f"metadata-form-{editing_pid}"):
                meta_col1, meta_col2 = st.columns(2)
                with meta_col1:
                    workstream = st.text_input("Workstream", value=display_info.get('workstream', ''), key=f"{editing_pid}-meta-workstream")
                    business_owner = st.text_input("Business Owner", value=display_info.get('business_owner', ''), key=f"{editing_pid}-meta-business_owner")
                    existing_users = st.text_area("Existing Users", value=display_info.get('existing_users', ''), key=f"{editing_pid}-meta-existing_users")
                    primary_operator = st.text_input("Primary Operator", value=display_info.get('primary_operator', ''), key=f"{editing_pid}-meta-primary_operator")
                with meta_col2:
                    primary_developer = st.text_input("Primary Developer", value=display_info.get('primary_developer', ''), key=f"{editing_pid}-meta-primary_developer")
                
                if st.form_submit_button("Save Product Information"):
                    metadata_update = {
                        'product_id': editing_pid,
                        'product_name': display_info.get('product_name', ''),
                        'workstream': workstream,
                        'business_owner': business_owner,
                        'existing_users': existing_users,
                        'primary_operator': primary_operator,
                        'primary_developer': primary_developer,
                    }
                    save_product_data(editing_pid, metadata_update)
                    st.success("Product information saved")
                    st.rerun()
        
        st.markdown("---")
        # Use product data directly
        existing = product_data

        def render_technical_form(existing):
            # Extract nested technical_session data
            tech_session = existing.get('technical_session', {}) if existing else {}
            part1 = tech_session.get('part1_overview', {})
            part2 = tech_session.get('part2_technical_stack', {})
            part3 = tech_session.get('part3_development_deployment', {})
            part4 = tech_session.get('part4_challenges', {})
            part5 = tech_session.get('part5_operation_deepdive', {})
            part5_usage = part5.get('usage_access', {})
            part5_pain = part5.get('pain_points_workarounds', {})
            part5_gap = part5.get('gap_analysis', {})
            part6 = tech_session.get('part6_data_integration', {})
            part6_inputs = part6.get('data_inputs', {})
            part6_outputs = part6.get('data_outputs', {})
            part6_storage = part6.get('data_storage', {})
            part6_integration = part6.get('integration_points', {})
            part7 = tech_session.get('part7_wrapup', {})
            part7_maturity = part7.get('maturity_scores', {})
            
            with st.form(f"edit-form-{editing_pid}-Technical"):
                st.write("Editing Technical session")
                
                st.markdown("### Session Data")
                if False:  # This is here to preserve the indentation for the technical section below
                    # Part 1: Context & Business Process
                    st.markdown("**Part 1: Context & Business Process**")
                    context_role = st.text_area("Role in technology delivery process", value=existing.get('context_role','') if existing else '', key=f"{editing_pid}-Technical-context_role")
                    context_stages = st.text_area("Stages involved", value=existing.get('context_stages','') if existing else '', key=f"{editing_pid}-Technical-context_stages")
                    context_decisions = st.text_area("Decisions made", value=existing.get('context_decisions','') if existing else '', key=f"{editing_pid}-Technical-context_decisions")
                    context_deliverables = st.text_area("Key deliverables", value=existing.get('context_deliverables','') if existing else '', key=f"{editing_pid}-Technical-context_deliverables")
                    context_workflow = st.text_area("Typical workflow/process", value=existing.get('context_workflow','') if existing else '', key=f"{editing_pid}-Technical-context_workflow")
                    context_steps = st.text_area("Workflow steps", value=existing.get('context_steps','') if existing else '', key=f"{editing_pid}-Technical-context_steps")
                    context_info_needed = st.text_area("Information needed at each step", value=existing.get('context_info_needed','') if existing else '', key=f"{editing_pid}-Technical-context_info_needed")
                    context_decision_points = st.text_area("Decision points", value=existing.get('context_decision_points','') if existing else '', key=f"{editing_pid}-Technical-context_decision_points")
                    context_partner_impact = st.text_area("Impact on partner timeline", value=existing.get('context_partner_impact','') if existing else '', key=f"{editing_pid}-Technical-context_partner_impact")
                    context_partner_confidence = st.text_area("What builds partner confidence", value=existing.get('context_partner_confidence','') if existing else '', key=f"{editing_pid}-Technical-context_partner_confidence")
                    context_partner_frustration = st.text_area("Where partners get frustrated", value=existing.get('context_partner_frustration','') if existing else '', key=f"{editing_pid}-Technical-context_partner_frustration")

                    # Part 2: Product Portfolio Review
                    st.markdown("**Part 2: Product Portfolio Review**")
                    product_purpose = st.text_area("Purpose of product", value=existing.get('product_purpose','') if existing else '', key=f"{editing_pid}-Technical-product_purpose")
                    product_why_created = st.text_area("Why was it created?", value=existing.get('product_why_created','') if existing else '', key=f"{editing_pid}-Technical-product_why_created")
                    product_impact = st.text_area("Business impact when product works well vs not", value=existing.get('product_impact','') if existing else '', key=f"{editing_pid}-Technical-product_impact")
                    product_time_saved = st.text_area("Time saved/lost", value=existing.get('product_time_saved','') if existing else '', key=f"{editing_pid}-Technical-product_time_saved")
                    product_quality = st.text_area("Quality of decisions", value=existing.get('product_quality','') if existing else '', key=f"{editing_pid}-Technical-product_quality")
                    product_partner_confidence = st.text_area("Partner confidence", value=existing.get('product_partner_confidence','') if existing else '', key=f"{editing_pid}-Technical-product_partner_confidence")

                    # Section B.1: Use overview
                    st.markdown("**Section B.1: Use overview**")
                    use_purpose = st.text_area("What do you use the product for?", value=existing.get('use_purpose','') if existing else '', key=f"{editing_pid}-Technical-use_purpose")
                    use_frequency = st.text_area("How often do you use it?", value=existing.get('use_frequency','') if existing else '', key=f"{editing_pid}-Technical-use_frequency")
                    use_who = st.text_area("Who else uses it?", value=existing.get('use_who','') if existing else '', key=f"{editing_pid}-Technical-use_who")
                    use_workflow_stage = st.text_area("Where does this fit in your workflow?", value=existing.get('use_workflow_stage','') if existing else '', key=f"{editing_pid}-Technical-use_workflow_stage")
                    use_decisions = st.text_area("What decisions do you make based on this product's outputs?", value=existing.get('use_decisions','') if existing else '', key=f"{editing_pid}-Technical-use_decisions")
                    use_critical = st.text_area("Are those critical decisions?", value=existing.get('use_critical','') if existing else '', key=f"{editing_pid}-Technical-use_critical")
                    use_confidence = st.text_area("Do you have confidence in the outputs?", value=existing.get('use_confidence','') if existing else '', key=f"{editing_pid}-Technical-use_confidence")
                    use_decisions_without = st.text_area("Have you ever made decisions without this product? Why?", value=existing.get('use_decisions_without','') if existing else '', key=f"{editing_pid}-Technical-use_decisions_without")
                    use_not_direct = st.text_area("Why do you not use this product directly?", value=existing.get('use_not_direct','') if existing else '', key=f"{editing_pid}-Technical-use_not_direct")

                    # Section B.2: Pain Points & Gaps
                    st.markdown("**Section B.2: Pain Points & Gaps**")
                    pain_frustrations = st.text_area("What frustrates you about this product or process?", value=existing.get('pain_frustrations','') if existing else '', key=f"{editing_pid}-Technical-pain_frustrations")
                    pain_slows = st.text_area("What slows you down?", value=existing.get('pain_slows','') if existing else '', key=f"{editing_pid}-Technical-pain_slows")
                    pain_extra_work = st.text_area("What creates extra work?", value=existing.get('pain_extra_work','') if existing else '', key=f"{editing_pid}-Technical-pain_extra_work")
                    pain_rework = st.text_area("What causes rework or errors?", value=existing.get('pain_rework','') if existing else '', key=f"{editing_pid}-Technical-pain_rework")
                    pain_missing_content = st.text_area("Are the outputs accurate, complete, useful?", value=existing.get('pain_missing_content','') if existing else '', key=f"{editing_pid}-Technical-pain_missing_content")
                    pain_timeline = st.text_area("Does it deliver results fast enough?", value=existing.get('pain_timeline','') if existing else '', key=f"{editing_pid}-Technical-pain_timeline")
                    pain_usability = st.text_area("Is it easy to use or does it require special skills?", value=existing.get('pain_usability','') if existing else '', key=f"{editing_pid}-Technical-pain_usability")
                    pain_info_needed = st.text_area("Information you need but can't get?", value=existing.get('pain_info_needed','') if existing else '', key=f"{editing_pid}-Technical-pain_info_needed")
                    pain_decisions_needed = st.text_area("Decisions you need to make but lack data for?", value=existing.get('pain_decisions_needed','') if existing else '', key=f"{editing_pid}-Technical-pain_decisions_needed")
                    pain_manual_work = st.text_area("Manual work you do that should be automated?", value=existing.get('pain_manual_work','') if existing else '', key=f"{editing_pid}-Technical-pain_manual_work")
                    pain_workarounds = st.text_area("Do you have workarounds or manual processes to deal with limitations?", value=existing.get('pain_workarounds','') if existing else '', key=f"{editing_pid}-Technical-pain_workarounds")
                    pain_time_added = st.text_area("How much time do they add?", value=existing.get('pain_time_added','') if existing else '', key=f"{editing_pid}-Technical-pain_time_added")
                    pain_why_necessary = st.text_area("Why are they necessary?", value=existing.get('pain_why_necessary','') if existing else '', key=f"{editing_pid}-Technical-pain_why_necessary")

                else:
                    # Technical session — comprehensive form per provided structure
                    with st.expander("Part 1: Developer’s Product Overview", expanded=False):
                        overview_product_desc = st.text_area("What is the product and why does it exist?", value=(part1.get('overview_product_desc', '') if existing else ''), key=f"{editing_pid}-Technical-overview_product_desc")
                        overview_problem_solved = st.text_area("What problems does it solve?", value=(part1.get('overview_problem_solved', '') if existing else ''), key=f"{editing_pid}-Technical-overview_problem_solved")
                        overview_process_fit = st.text_area("Where does it fit in the delivery process?", value=(part1.get('overview_process_fit', '') if existing else ''), key=f"{editing_pid}-Technical-overview_process_fit")

                        overview_history = st.text_area("History & evolution", value=(part1.get('overview_history', '') if existing else ''), key=f"{editing_pid}-Technical-overview_history")
                        overview_alignment = st.text_area("Alignment notes from other participants", value=(part1.get('overview_alignment', '') if existing else ''), key=f"{editing_pid}-Technical-overview_alignment")

                    with st.expander("Part 2: Development Deep-Dive", expanded=False):
                        st.markdown("#### A. Technical Stack")
                        tech_languages_versions = st.text_area("Languages & versions", value=(part2.get('tech_languages_versions', '') if existing else ''), key=f"{editing_pid}-Technical-tech_languages_versions")
                        tech_frameworks_libs = st.text_area("Frameworks & libraries", value=(part2.get('tech_frameworks_libs', '') if existing else ''), key=f"{editing_pid}-Technical-tech_frameworks_libs")
                        tech_commercial_tools = st.text_area("Commercial packages/tools", value=(part2.get('tech_commercial_tools', '') if existing else ''), key=f"{editing_pid}-Technical-tech_commercial_tools")
                        tech_dependencies_external = st.text_area("External dependencies/services", value=(part2.get('tech_dependencies_external', '') if existing else ''), key=f"{editing_pid}-Technical-tech_dependencies_external")
                        tech_dependencies_internal = st.text_area("Internal dependencies (Nuton systems)", value=(part2.get('tech_dependencies_internal', '') if existing else ''), key=f"{editing_pid}-Technical-tech_dependencies_internal")
                        tech_runtime_env = st.text_area("Intended runtime (local/server/cloud)", value=(part2.get('tech_runtime_env', '') if existing else ''), key=f"{editing_pid}-Technical-tech_runtime_env")
                        tech_os_requirements = st.text_area("OS requirements", value=(part2.get('tech_os_requirements', '') if existing else ''), key=f"{editing_pid}-Technical-tech_os_requirements")
                        tech_hardware_needs = st.text_area("Special hardware needs", value=(part2.get('tech_hardware_needs', '') if existing else ''), key=f"{editing_pid}-Technical-tech_hardware_needs")

                        st.markdown("#### B. Development Environment & Practices")
                        dev_feature_request = st.text_area("How are features requested and prioritized?", value=(part3.get('dev_feature_request', '') if existing else ''), key=f"{editing_pid}-Technical-dev_feature_request")
                        dev_roadmap = st.text_area("Roadmap (exists/how managed)", value=(part3.get('dev_roadmap', '') if existing else ''), key=f"{editing_pid}-Technical-dev_roadmap")
                        dev_version_control = st.text_area("Version control (tool/location)", value=(part3.get('dev_version_control', '') if existing else ''), key=f"{editing_pid}-Technical-dev_version_control")
                        dev_code_reviews = st.text_area("Code reviews", value=(part3.get('dev_code_reviews', '') if existing else ''), key=f"{editing_pid}-Technical-dev_code_reviews")
                        dev_testing = st.text_area("Testing approach (unit/integration/regression/manual)", value=(part3.get('dev_testing', '') if existing else ''), key=f"{editing_pid}-Technical-dev_testing")
                        dev_docs = st.text_area("Documentation approach", value=(part3.get('dev_docs', '') if existing else ''), key=f"{editing_pid}-Technical-dev_docs")
                        dev_deploy_process = st.text_area("Deploy process & frequency", value=(part3.get('dev_deploy_process', '') if existing else ''), key=f"{editing_pid}-Technical-dev_deploy_process")
                        dev_deploy_roles = st.text_area("Who can deploy", value=(part3.get('dev_deploy_roles', '') if existing else ''), key=f"{editing_pid}-Technical-dev_deploy_roles")
                        dev_deploy_duration = st.text_area("Deployment duration", value=(part3.get('dev_deploy_duration', '') if existing else ''), key=f"{editing_pid}-Technical-dev_deploy_duration")
                        dev_operator_coordination = st.text_area("Coordination with Operators during deploys", value=(part3.get('dev_operator_coordination', '') if existing else ''), key=f"{editing_pid}-Technical-dev_operator_coordination")
                        dev_operator_comms = st.text_area("Operator comms about changes", value=(part3.get('dev_operator_comms', '') if existing else ''), key=f"{editing_pid}-Technical-dev_operator_comms")

                        st.markdown("#### C. Technical Challenges")
                        challenges_limitations = st.text_area("Technical limitations/constraints", value=(part4.get('challenges_limitations', '') if existing else ''), key=f"{editing_pid}-Technical-challenges_limitations")
                        challenges_rewrite = st.text_area("What would you do differently if rebuilding?", value=(part4.get('challenges_rewrite', '') if existing else ''), key=f"{editing_pid}-Technical-challenges_rewrite")
                        challenges_tech_debt = st.text_area("Technical debt / issues", value=(part4.get('challenges_tech_debt', '') if existing else ''), key=f"{editing_pid}-Technical-challenges_tech_debt")
                        challenges_maintainability = st.text_area("Who else could maintain / training time", value=(part4.get('challenges_maintainability', '') if existing else ''), key=f"{editing_pid}-Technical-challenges_maintainability")
                        challenges_docs_training = st.text_area("Docs availability / training", value=(part4.get('challenges_docs_training', '') if existing else ''), key=f"{editing_pid}-Technical-challenges_docs_training")

                    with st.expander("Part 3: Operation Deep-Dive", expanded=False):
                        st.markdown("#### A. Usage & Access")
                        usage_frequency = st.text_area("Usage frequency (daily/weekly/per project)", value=(part5_usage.get('usage_frequency', '') if existing else ''), key=f"{editing_pid}-Technical-usage_frequency")
                        usage_tasks = st.text_area("Tasks performed", value=(part5_usage.get('usage_tasks', '') if existing else ''), key=f"{editing_pid}-Technical-usage_tasks")
                        usage_duration = st.text_area("Typical duration", value=(part5_usage.get('usage_duration', '') if existing else ''), key=f"{editing_pid}-Technical-usage_duration")
                        access_method = st.text_area("Access method (desktop/web/CLI)", value=(part5_usage.get('access_method', '') if existing else ''), key=f"{editing_pid}-Technical-access_method")
                        access_permissions = st.text_area("Access/permissions needed", value=(part5_usage.get('access_permissions', '') if existing else ''), key=f"{editing_pid}-Technical-access_permissions")
                        access_locations = st.text_area("Locations usable (any/specific)", value=(part5_usage.get('access_locations', '') if existing else ''), key=f"{editing_pid}-Technical-access_locations")
                        training_type = st.text_area("Training type & provider", value=(part5_usage.get('training_type', '') if existing else ''), key=f"{editing_pid}-Technical-training_type")
                        training_duration = st.text_area("Time to proficiency", value=(part5_usage.get('training_duration', '') if existing else ''), key=f"{editing_pid}-Technical-training_duration")
                        training_docs = st.text_area("Docs/user guides availability", value=(part5_usage.get('training_docs', '') if existing else ''), key=f"{editing_pid}-Technical-training_docs")

                        st.markdown("#### B. Pain Points & Workarounds")
                        ops_pain_points = st.text_area("Biggest frustrations", value=(part5_pain.get('ops_pain_points', '') if existing else ''), key=f"{editing_pid}-Technical-ops_pain_points")
                        ops_slowdowns = st.text_area("Where it slows you down / extra work", value=(part5_pain.get('ops_slowdowns', '') if existing else ''), key=f"{editing_pid}-Technical-ops_slowdowns")
                        ops_workarounds = st.text_area("Workarounds / manual steps", value=(part5_pain.get('ops_workarounds', '') if existing else ''), key=f"{editing_pid}-Technical-ops_workarounds")
                        ops_failure_detection = st.text_area("Failure detection (how you know)", value=(part5_pain.get('ops_failure_detection', '') if existing else ''), key=f"{editing_pid}-Technical-ops_failure_detection")
                        ops_self_debug = st.text_area("Self-debug info used", value=(part5_pain.get('ops_self_debug', '') if existing else ''), key=f"{editing_pid}-Technical-ops_self_debug")
                        ops_support_contact = st.text_area("Who you contact for help", value=(part5_pain.get('ops_support_contact', '') if existing else ''), key=f"{editing_pid}-Technical-ops_support_contact")
                        ops_resolution_time = st.text_area("Typical resolution time", value=(part5_pain.get('ops_resolution_time', '') if existing else ''), key=f"{editing_pid}-Technical-ops_resolution_time")
                        ops_missing_features = st.text_area("Missing features / wishlist", value=(part5_pain.get('ops_missing_features', '') if existing else ''), key=f"{editing_pid}-Technical-ops_missing_features")

                        st.markdown("#### C. Gap Analysis")
                        gap_output_quality = st.text_area("Output content/quality sufficiency", value=(part5_gap.get('gap_output_quality', '') if existing else ''), key=f"{editing_pid}-Technical-gap_output_quality")
                        gap_timeline_speed = st.text_area("Timeline/speed sufficiency", value=(part5_gap.get('gap_timeline_speed', '') if existing else ''), key=f"{editing_pid}-Technical-gap_timeline_speed")
                        gap_unavailability = st.text_area("Times you need but can't use; why", value=(part5_gap.get('gap_unavailability', '') if existing else ''), key=f"{editing_pid}-Technical-gap_unavailability")
                        gap_alternatives = st.text_area("Alternative methods used; when/why", value=(part5_gap.get('gap_alternatives', '') if existing else ''), key=f"{editing_pid}-Technical-gap_alternatives")

                    with st.expander("Part 4: Data and Integration", expanded=False):
                        st.markdown("#### A. Data Inputs")
                        data_inputs_sources = st.text_area("Sources", value=(part6_inputs.get('data_inputs_sources', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_sources")
                        data_inputs_format = st.text_area("Formats", value=(part6_inputs.get('data_inputs_format', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_format")
                        data_inputs_frequency = st.text_area("Frequency", value=(part6_inputs.get('data_inputs_frequency', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_frequency")
                        data_inputs_ingestion = st.text_area("Ingestion process (auto/manual)", value=(part6_inputs.get('data_inputs_ingestion', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_ingestion")
                        data_inputs_time = st.text_area("Time to ingest", value=(part6_inputs.get('data_inputs_time', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_time")
                        data_inputs_prep = st.text_area("Preparation/cleaning", value=(part6_inputs.get('data_inputs_prep', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_prep")
                        data_inputs_failure = st.text_area("Behavior if wrong/missing/delayed", value=(part6_inputs.get('data_inputs_failure', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_failure")
                        data_inputs_volume = st.text_area("Volume (records, sizes)", value=(part6_inputs.get('data_inputs_volume', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_volume")
                        data_inputs_growth = st.text_area("Growth rate", value=(part6_inputs.get('data_inputs_growth', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_growth")
                        data_inputs_retention = st.text_area("Retention (how long kept)", value=(part6_inputs.get('data_inputs_retention', '') if existing else ''), key=f"{editing_pid}-Technical-data_inputs_retention")

                        st.markdown("#### B. Data Outputs")
                        data_outputs_types = st.text_area("Outputs produced", value=(part6_outputs.get('data_outputs_types', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_types")
                        data_outputs_destinations = st.text_area("Destinations / consumers", value=(part6_outputs.get('data_outputs_destinations', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_destinations")
                        data_outputs_format = st.text_area("Formats & delivery", value=(part6_outputs.get('data_outputs_format', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_format")
                        data_outputs_export = st.text_area("Export process; time; reformatting", value=(part6_outputs.get('data_outputs_export', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_export")
                        data_outputs_post = st.text_area("Post-process usage", value=(part6_outputs.get('data_outputs_post', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_post")
                        data_outputs_retention = st.text_area("Output retention", value=(part6_outputs.get('data_outputs_retention', '') if existing else ''), key=f"{editing_pid}-Technical-data_outputs_retention")

                        st.markdown("#### C. Data Storage")
                        data_storage_locations = st.text_area("Storage locations (DB, Databricks, filesystem)", value=(part6_storage.get('data_storage_locations', '') if existing else ''), key=f"{editing_pid}-Technical-data_storage_locations")
                        data_storage_access = st.text_area("Access controls", value=(part6_storage.get('data_storage_access', '') if existing else ''), key=f"{editing_pid}-Technical-data_storage_access")
                        data_storage_backup = st.text_area("Backup approach", value=(part6_storage.get('data_storage_backup', '') if existing else ''), key=f"{editing_pid}-Technical-data_storage_backup")
                        data_storage_recovery = st.text_area("Recovery approach", value=(part6_storage.get('data_storage_recovery', '') if existing else ''), key=f"{editing_pid}-Technical-data_storage_recovery")

                        st.markdown("#### D. Integration Points")
                        integrations_nuton = st.text_area("Nuton products/systems integrations & reliability", value=(part6_integration.get('integrations_nuton', '') if existing else ''), key=f"{editing_pid}-Technical-integrations_nuton")
                        integrations_external = st.text_area("External systems integrations (Databricks/PI/AVEVA/etc)", value=(part6_integration.get('integrations_external', '') if existing else ''), key=f"{editing_pid}-Technical-integrations_external")
                        integrations_desired = st.text_area("Desired integrations not present", value=(part6_integration.get('integrations_desired', '') if existing else ''), key=f"{editing_pid}-Technical-integrations_desired")

                    with st.expander("Part 5: Wrap-Up", expanded=False):
                        # Maturity scoring sliders (1–5)
                        maturity_dev_default = 3
                        maturity_ops_default = 3
                        maturity_data_default = 3
                        maturity_integ_default = 3
                        maturity_docs_default = 3
                        if existing:
                            try:
                                maturity_dev_default = int(existing.get('maturity_development', maturity_dev_default))
                            except Exception:
                                pass
                            try:
                                maturity_ops_default = int(existing.get('maturity_operational', maturity_ops_default))
                            except Exception:
                                pass
                            try:
                                maturity_data_default = int(existing.get('maturity_data', maturity_data_default))
                            except Exception:
                                pass
                            try:
                                maturity_integ_default = int(existing.get('maturity_integration', maturity_integ_default))
                            except Exception:
                                pass
                            try:
                                maturity_docs_default = int(existing.get('maturity_documentation', maturity_docs_default))
                            except Exception:
                                pass

                        maturity_development = st.slider("Development maturity (1–5)", min_value=1, max_value=5, value=maturity_dev_default, key=f"{editing_pid}-Technical-maturity_development")
                        maturity_operational = st.slider("Operational maturity (1–5)", min_value=1, max_value=5, value=maturity_ops_default, key=f"{editing_pid}-Technical-maturity_operational")
                        maturity_data = st.slider("Data maturity (1–5)", min_value=1, max_value=5, value=maturity_data_default, key=f"{editing_pid}-Technical-maturity_data")
                        maturity_integration = st.slider("Integration maturity (1–5)", min_value=1, max_value=5, value=maturity_integ_default, key=f"{editing_pid}-Technical-maturity_integration")
                        maturity_documentation = st.slider("Documentation maturity (1–5)", min_value=1, max_value=5, value=maturity_docs_default, key=f"{editing_pid}-Technical-maturity_documentation")

                        prioritization_improvement = st.text_area("One thing to fix/improve", value=(part7.get('prioritization_improvement', '') if existing else ''), key=f"{editing_pid}-Technical-prioritization_improvement")
                        critical_unknowns = st.text_area("Critical unknowns not asked", value=(part7.get('critical_unknowns', '') if existing else ''), key=f"{editing_pid}-Technical-critical_unknowns")
                        predict_platform_fit = st.text_area("Fit to Predict platform vision", value=(part7.get('predict_platform_fit', '') if existing else ''), key=f"{editing_pid}-Technical-predict_platform_fit")
                        summary_validation = st.text_area("Summary/validation notes", value=(part7.get('summary_validation', '') if existing else ''), key=f"{editing_pid}-Technical-summary_validation")
                        quotes = st.text_area("Verbatim quotes (Speaker | timestamp | quote per line)", value='\n'.join([f"{q.get('speaker')}|{q.get('timestamp')}|{q.get('quote')}" for q in part7.get('quotes', [])]) if existing else '', key=f"{editing_pid}-Technical-quotes")

                submitted = st.form_submit_button("Save Technical session")
                if submitted:
                    # Parse quotes
                    qs = []
                    for line in quotes.splitlines():
                        if not line.strip():
                            continue
                        parts = [p.strip() for p in line.split("|")]
                        qs.append({'speaker': parts[0] if parts else '', 'timestamp': parts[1] if len(parts)>1 else '', 'quote': parts[2] if len(parts)>2 else parts[-1]})
                    
                    # Build nested technical_session structure
                    product_data = {
                        'product_id': editing_pid,
                        'product_name': display_info.get('product_name', ''),
                        'technical_session': {
                            'part1_overview': {
                                'overview_product_desc': overview_product_desc,
                                'overview_problem_solved': overview_problem_solved,
                                'overview_process_fit': overview_process_fit,
                                'overview_history': overview_history,
                                'overview_alignment': overview_alignment,
                            },
                            'part2_technical_stack': {
                                'tech_languages_versions': tech_languages_versions,
                                'tech_frameworks_libs': tech_frameworks_libs,
                                'tech_commercial_tools': tech_commercial_tools,
                                'tech_dependencies_external': tech_dependencies_external,
                                'tech_dependencies_internal': tech_dependencies_internal,
                                'tech_runtime_env': tech_runtime_env,
                                'tech_os_requirements': tech_os_requirements,
                                'tech_hardware_needs': tech_hardware_needs,
                            },
                            'part3_development_deployment': {
                                'dev_feature_request': dev_feature_request,
                                'dev_roadmap': dev_roadmap,
                                'dev_version_control': dev_version_control,
                                'dev_code_reviews': dev_code_reviews,
                                'dev_testing': dev_testing,
                                'dev_docs': dev_docs,
                                'dev_deploy_process': dev_deploy_process,
                                'dev_deploy_roles': dev_deploy_roles,
                                'dev_deploy_duration': dev_deploy_duration,
                                'dev_operator_coordination': dev_operator_coordination,
                                'dev_operator_comms': dev_operator_comms,
                            },
                            'part4_challenges': {
                                'challenges_limitations': challenges_limitations,
                                'challenges_rewrite': challenges_rewrite,
                                'challenges_tech_debt': challenges_tech_debt,
                                'challenges_maintainability': challenges_maintainability,
                                'challenges_docs_training': challenges_docs_training,
                            },
                            'part5_operation_deepdive': {
                                'usage_access': {
                                    'usage_frequency': usage_frequency,
                                    'usage_tasks': usage_tasks,
                                    'usage_duration': usage_duration,
                                    'access_method': access_method,
                                    'access_permissions': access_permissions,
                                    'access_locations': access_locations,
                                    'training_type': training_type,
                                    'training_duration': training_duration,
                                    'training_docs': training_docs,
                                },
                                'pain_points_workarounds': {
                                    'ops_pain_points': ops_pain_points,
                                    'ops_slowdowns': ops_slowdowns,
                                    'ops_workarounds': ops_workarounds,
                                    'ops_failure_detection': ops_failure_detection,
                                    'ops_self_debug': ops_self_debug,
                                    'ops_support_contact': ops_support_contact,
                                    'ops_resolution_time': ops_resolution_time,
                                    'ops_missing_features': ops_missing_features,
                                },
                                'gap_analysis': {
                                    'gap_output_quality': gap_output_quality,
                                    'gap_timeline_speed': gap_timeline_speed,
                                    'gap_unavailability': gap_unavailability,
                                    'gap_alternatives': gap_alternatives,
                                },
                            },
                            'part6_data_integration': {
                                'data_inputs': {
                                    'data_inputs_sources': data_inputs_sources,
                                    'data_inputs_format': data_inputs_format,
                                    'data_inputs_frequency': data_inputs_frequency,
                                    'data_inputs_ingestion': data_inputs_ingestion,
                                    'data_inputs_time': data_inputs_time,
                                    'data_inputs_prep': data_inputs_prep,
                                    'data_inputs_failure': data_inputs_failure,
                                    'data_inputs_volume': data_inputs_volume,
                                    'data_inputs_growth': data_inputs_growth,
                                    'data_inputs_retention': data_inputs_retention,
                                },
                                'data_outputs': {
                                    'data_outputs_types': data_outputs_types,
                                    'data_outputs_destinations': data_outputs_destinations,
                                    'data_outputs_format': data_outputs_format,
                                    'data_outputs_export': data_outputs_export,
                                    'data_outputs_post': data_outputs_post,
                                    'data_outputs_retention': data_outputs_retention,
                                },
                                'data_storage': {
                                    'data_storage_locations': data_storage_locations,
                                    'data_storage_access': data_storage_access,
                                    'data_storage_backup': data_storage_backup,
                                    'data_storage_recovery': data_storage_recovery,
                                },
                                'integration_points': {
                                    'integrations_nuton': integrations_nuton,
                                    'integrations_external': integrations_external,
                                    'integrations_desired': integrations_desired,
                                },
                            },
                            'part7_wrapup': {
                                'maturity_scores': {
                                    'maturity_development': maturity_development,
                                    'maturity_operational': maturity_operational,
                                    'maturity_data': maturity_data,
                                    'maturity_integration': maturity_integration,
                                    'maturity_documentation': maturity_documentation,
                                },
                                'prioritization_improvement': prioritization_improvement,
                                'critical_unknowns': critical_unknowns,
                                'predict_platform_fit': predict_platform_fit,
                                'summary_validation': summary_validation,
                                'quotes': qs,
                            },
                        },
                    }
                    
                    save_product_data(editing_pid, product_data)
                    st.success("Saved Technical data for product")
                    st.rerun()

        # Render only Technical form
        with st.expander("Technical Session (Operator/Developer)", expanded=True):
            render_technical_form(existing)

    elif page == 'Business Owner Sessions':
        st.header("Business Owner / User Sessions")
        st.markdown("Edit business session data at the business owner level. Each session covers all products owned by that business owner.")
        
        csv_products = load_products_from_csv()
        if not csv_products:
            st.warning("Could not load products from CSV.")
            return
        
        # Group products by business owner
        owner_groups = {}
        for prod in csv_products:
            owner = prod.get('business_owner', 'Unassigned')
            if owner not in owner_groups:
                owner_groups[owner] = []
            owner_groups[owner].append(prod)
        
        # Select business owner
        selected_owner = st.selectbox(
            "Select Business Owner",
            options=sorted(owner_groups.keys()),
            key='business_owner_select'
        )
        
        if not selected_owner:
            return
        
        products_for_owner = owner_groups[selected_owner]
        
        st.markdown(f"### Business Owner: {selected_owner}")
        st.markdown(f"**Products covered in this session ({len(products_for_owner)}):**")
        for prod in products_for_owner:
            st.write(f"- {prod['product_name']}")
        
        st.markdown("---")
        
        # Load existing business owner data
        existing_session = get_business_owner_data(selected_owner)
        
        # Business session form
        with st.form(f"business-session-{slugify(selected_owner)}"):
            st.markdown("### Business Owner / User Session")
            
            # Extract nested data
            part1 = existing_session.get('part1_context_business_process', {}) if existing_session else {}
            part2 = existing_session.get('part2_product_portfolio_review', {}) if existing_session else {}
            part2a = part2.get('section_a_business_owner', {}) if part2 else {}
            part2b = part2.get('section_b_users', {}) if part2 else {}
            part2b1 = part2b.get('b1_use_overview', {}) if part2b else {}
            part2b2 = part2b.get('b2_pain_points_gaps', {}) if part2b else {}
            part3 = existing_session.get('part3_cross_product_process', {}) if existing_session else {}
            part3a = part3.get('section_a_integration', {}) if part3 else {}
            part3b = part3.get('section_b_bottlenecks', {}) if part3 else {}
            part4 = existing_session.get('part4_partner_delivery', {}) if existing_session else {}
            part4a = part4.get('section_a_info_needs', {}) if part4 else {}
            part4b = part4.get('section_b_confidence_trust', {}) if part4 else {}
            part5 = existing_session.get('part5_ideal_future_state', {}) if existing_session else {}
            part5a = part5.get('section_a_prioritization', {}) if part5 else {}
            part5b = part5.get('section_b_vision', {}) if part5 else {}
            part5c = part5.get('section_c_capabilities', {}) if part5 else {}
            part6 = existing_session.get('part6_wrapup', {}) if existing_session else {}
            
            with st.expander("Part 1: Context & Business Process (15m)", expanded=False):
                st.markdown("**Purpose:** Establish business context and how this product family fits into technology delivery")
                context_role = st.text_area("What's your role in the technology delivery process?", value=part1.get('context_role',''), key=f"{selected_owner}-context_role")
                context_stages = st.text_area("Which stage(s)?", value=part1.get('context_stages',''), key=f"{selected_owner}-context_stages")
                context_decisions = st.text_area("What decisions do you make?", value=part1.get('context_decisions',''), key=f"{selected_owner}-context_decisions")
                context_deliverables = st.text_area("What are your key deliverables?", value=part1.get('context_deliverables',''), key=f"{selected_owner}-context_deliverables")
                st.markdown("**Walk me through your typical workflow or process**")
                context_workflow = st.text_area("Typical workflow/process", value=part1.get('context_workflow',''), key=f"{selected_owner}-context_workflow")
                context_steps = st.text_area("What are the steps?", value=part1.get('context_steps',''), key=f"{selected_owner}-context_steps")
                context_info_needed = st.text_area("What information do you need at each step?", value=part1.get('context_info_needed',''), key=f"{selected_owner}-context_info_needed")
                context_decision_points = st.text_area("Where do decisions get made?", value=part1.get('context_decision_points',''), key=f"{selected_owner}-context_decision_points")
                st.markdown("**How does this work relate to partnership delivery?**")
                context_partner_impact = st.text_area("How does your work impact partner timeline?", value=part1.get('context_partner_impact',''), key=f"{selected_owner}-context_partner_impact")
                context_partner_confidence = st.text_area("What builds partner confidence?", value=part1.get('context_partner_confidence',''), key=f"{selected_owner}-context_partner_confidence")
                context_partner_frustration = st.text_area("Where do partners get frustrated or concerned?", value=part1.get('context_partner_frustration',''), key=f"{selected_owner}-context_partner_frustration")
            
            with st.expander("Part 2: Product Portfolio Review (30m)", expanded=False):
                st.markdown("**Section A: Business Owner**")
                product_purpose = st.text_area("What is the purpose of these products?", value=part2a.get('product_purpose',''), key=f"{selected_owner}-product_purpose")
                product_why_created = st.text_area("Why were they created?", value=part2a.get('product_why_created',''), key=f"{selected_owner}-product_why_created")
                product_what_achieve = st.text_area("What are they used to achieve?", value=part2a.get('product_what_achieve',''), key=f"{selected_owner}-product_what_achieve")
                st.markdown("**What's the business impact when products work well vs. when they don't?**")
                product_impact_works_well = st.text_area("When products work well", value=part2a.get('product_impact_works_well',''), key=f"{selected_owner}-product_impact_works_well")
                product_impact_doesnt_work = st.text_area("When products don't work", value=part2a.get('product_impact_doesnt_work',''), key=f"{selected_owner}-product_impact_doesnt_work")
                product_time_impact = st.text_area("Time saved/lost?", value=part2a.get('product_time_impact',''), key=f"{selected_owner}-product_time_impact")
                product_quality_decisions = st.text_area("Quality of decisions?", value=part2a.get('product_quality_decisions',''), key=f"{selected_owner}-product_quality_decisions")
                product_partner_confidence = st.text_area("Partner confidence?", value=part2a.get('product_partner_confidence',''), key=f"{selected_owner}-product_partner_confidence")
                
                st.markdown("---")
                st.markdown("**Section B: Users - B.1 Use Overview**")
                use_purpose = st.text_area("What do you use these products for? (Specific business purpose)", value=part2b1.get('use_purpose',''), key=f"{selected_owner}-use_purpose")
                use_frequency = st.text_area("How often do you use them?", value=part2b1.get('use_frequency',''), key=f"{selected_owner}-use_frequency")
                use_who_else = st.text_area("Who else uses them?", value=part2b1.get('use_who_else',''), key=f"{selected_owner}-use_who_else")
                use_workflow_stage = st.text_area("Where does this fit in your workflow? (Which stage of technology delivery?)", value=part2b1.get('use_workflow_stage',''), key=f"{selected_owner}-use_workflow_stage")
                use_critical_path = st.text_area("Is it critical path or supporting?", value=part2b1.get('use_critical_path',''), key=f"{selected_owner}-use_critical_path")
                use_decisions = st.text_area("What decisions do you make based on product outputs?", value=part2b1.get('use_decisions',''), key=f"{selected_owner}-use_decisions")
                use_decision_explanation = st.text_area("How do you make decisions based on the artefact?", value=part2b1.get('use_decision_explanation',''), key=f"{selected_owner}-use_decision_explanation")
                use_critical_decisions = st.text_area("Are those critical decisions?", value=part2b1.get('use_critical_decisions',''), key=f"{selected_owner}-use_critical_decisions")
                use_confidence_outputs = st.text_area("Do you have confidence in the outputs?", value=part2b1.get('use_confidence_outputs',''), key=f"{selected_owner}-use_confidence_outputs")
                use_decisions_without_product = st.text_area("Have you ever made decisions without this product? Why?", value=part2b1.get('use_decisions_without_product',''), key=f"{selected_owner}-use_decisions_without_product")
                use_why_not_direct = st.text_area("Why do you not use this product directly?", value=part2b1.get('use_why_not_direct',''), key=f"{selected_owner}-use_why_not_direct")
                
                st.markdown("---")
                st.markdown("**Section B: Users - B.2 Pain Points & Gaps**")
                pain_frustrations = st.text_area("What frustrates you about this product or process?", value=part2b2.get('pain_frustrations',''), key=f"{selected_owner}-pain_frustrations")
                pain_slowdowns = st.text_area("What slows you down?", value=part2b2.get('pain_slowdowns',''), key=f"{selected_owner}-pain_slowdowns")
                pain_extra_work = st.text_area("What creates extra work?", value=part2b2.get('pain_extra_work',''), key=f"{selected_owner}-pain_extra_work")
                pain_rework_errors = st.text_area("What causes rework or errors?", value=part2b2.get('pain_rework_errors',''), key=f"{selected_owner}-pain_rework_errors")
                st.markdown("**Are there things you need to do that this product doesn't support?**")
                pain_unsupported_needs = st.text_area("Things product doesn't support", value=part2b2.get('pain_unsupported_needs',''), key=f"{selected_owner}-pain_unsupported_needs")
                pain_content_quality = st.text_area("Content/Quality: Are outputs accurate, complete, useful?", value=part2b2.get('pain_content_quality',''), key=f"{selected_owner}-pain_content_quality")
                pain_timeline = st.text_area("Timeline: Does it deliver results fast enough?", value=part2b2.get('pain_timeline',''), key=f"{selected_owner}-pain_timeline")
                pain_usability = st.text_area("Usability: Is it easy to use or does it require special skills?", value=part2b2.get('pain_usability',''), key=f"{selected_owner}-pain_usability")
                pain_missing_info = st.text_area("Information you need but can't get?", value=part2b2.get('pain_missing_info',''), key=f"{selected_owner}-pain_missing_info")
                pain_missing_decisions = st.text_area("Decisions you need to make but lack data for?", value=part2b2.get('pain_missing_decisions',''), key=f"{selected_owner}-pain_missing_decisions")
                pain_manual_work = st.text_area("Manual work you do that should be automated?", value=part2b2.get('pain_manual_work',''), key=f"{selected_owner}-pain_manual_work")
                st.markdown("**Workarounds or manual processes**")
                pain_workarounds = st.text_area("What are your workarounds?", value=part2b2.get('pain_workarounds',''), key=f"{selected_owner}-pain_workarounds")
                pain_time_added = st.text_area("How much time do they add?", value=part2b2.get('pain_time_added',''), key=f"{selected_owner}-pain_time_added")
                pain_why_necessary = st.text_area("Why are they necessary?", value=part2b2.get('pain_why_necessary',''), key=f"{selected_owner}-pain_why_necessary")
            
            with st.expander("Part 3: Cross-Product & Process View (30m)", expanded=False):
                st.markdown("**Section A: Integration & Information Flow**")
                integration_products_work_together = st.text_area("How do these products work together in your workflow?", value=part3a.get('integration_products_work_together',''), key=f"{selected_owner}-integration_products_work_together")
                integration_manual_data_movement = st.text_area("Do you have to move data between them manually?", value=part3a.get('integration_manual_data_movement',''), key=f"{selected_owner}-integration_manual_data_movement")
                integration_gaps = st.text_area("Are there gaps where you need information from multiple products?", value=part3a.get('integration_gaps',''), key=f"{selected_owner}-integration_gaps")
                st.markdown("**Where do you need to combine information from different sources?**")
                integration_combine_info = st.text_area("Information combining needs", value=part3a.get('integration_combine_info',''), key=f"{selected_owner}-integration_combine_info")
                integration_how_combine = st.text_area("How do you do that today? (Excel, manually, not at all?)", value=part3a.get('integration_how_combine',''), key=f"{selected_owner}-integration_how_combine")
                integration_time_to_combine = st.text_area("How much time does that take?", value=part3a.get('integration_time_to_combine',''), key=f"{selected_owner}-integration_time_to_combine")
                integration_error_prone = st.text_area("Is it error-prone?", value=part3a.get('integration_error_prone',''), key=f"{selected_owner}-integration_error_prone")
                st.markdown("**Products/information outside this family**")
                integration_outside_products = st.text_area("Products or information sources outside this family that you also need?", value=part3a.get('integration_outside_products',''), key=f"{selected_owner}-integration_outside_products")
                integration_outside_fit = st.text_area("How do they fit in?", value=part3a.get('integration_outside_fit',''), key=f"{selected_owner}-integration_outside_fit")
                
                st.markdown("---")
                st.markdown("**Section B: Process Bottlenecks**")
                st.markdown("**Where does your process slow down or get stuck?**")
                bottleneck_where_slows = st.text_area("Where process slows down", value=part3b.get('bottleneck_where_slows',''), key=f"{selected_owner}-bottleneck_where_slows")
                bottleneck_waiting_info = st.text_area("Waiting for information?", value=part3b.get('bottleneck_waiting_info',''), key=f"{selected_owner}-bottleneck_waiting_info")
                bottleneck_manual_steps = st.text_area("Manual steps that take time?", value=part3b.get('bottleneck_manual_steps',''), key=f"{selected_owner}-bottleneck_manual_steps")
                bottleneck_rework = st.text_area("Rework because of errors?", value=part3b.get('bottleneck_rework',''), key=f"{selected_owner}-bottleneck_rework")
                bottleneck_handoffs = st.text_area("Handoffs to other teams?", value=part3b.get('bottleneck_handoffs',''), key=f"{selected_owner}-bottleneck_handoffs")
                st.markdown("**What takes longer than it should?**")
                bottleneck_takes_longer = st.text_area("What takes longer (site assessment, design iterations, reporting?)", value=part3b.get('bottleneck_takes_longer',''), key=f"{selected_owner}-bottleneck_takes_longer")
                bottleneck_why_long = st.text_area("Why does it take so long?", value=part3b.get('bottleneck_why_long',''), key=f"{selected_owner}-bottleneck_why_long")
                bottleneck_faster_look_like = st.text_area("What would faster look like?", value=part3b.get('bottleneck_faster_look_like',''), key=f"{selected_owner}-bottleneck_faster_look_like")
                st.markdown("**Where do partners experience delays?**")
                bottleneck_partner_delays = st.text_area("Partner delays", value=part3b.get('bottleneck_partner_delays',''), key=f"{selected_owner}-bottleneck_partner_delays")
                bottleneck_partner_waiting = st.text_area("What are they waiting for from you?", value=part3b.get('bottleneck_partner_waiting',''), key=f"{selected_owner}-bottleneck_partner_waiting")
                bottleneck_partner_frustrations = st.text_area("What frustrates them?", value=part3b.get('bottleneck_partner_frustrations',''), key=f"{selected_owner}-bottleneck_partner_frustrations")
            
            with st.expander("Part 4: Partner Delivery & External Perspective (15m)", expanded=False):
                st.markdown("**Section A: Partner Information Needs**")
                partner_info_needs = st.text_area("What information do partners need?", value=part4a.get('partner_info_needs',''), key=f"{selected_owner}-partner_info_needs")
                partner_info_frequency = st.text_area("How often?", value=part4a.get('partner_info_frequency',''), key=f"{selected_owner}-partner_info_frequency")
                partner_info_format = st.text_area("In what format?", value=part4a.get('partner_info_format',''), key=f"{selected_owner}-partner_info_format")
                st.markdown("**How do you deliver information to partners today?**")
                partner_delivery_method = st.text_area("Delivery method (reports, presentations, emails, phone calls?)", value=part4a.get('partner_delivery_method',''), key=f"{selected_owner}-partner_delivery_method")
                partner_delivery_time = st.text_area("How long does it take to prepare?", value=part4a.get('partner_delivery_time',''), key=f"{selected_owner}-partner_delivery_time")
                partner_delivery_automated = st.text_area("Is it manual or automated?", value=part4a.get('partner_delivery_automated',''), key=f"{selected_owner}-partner_delivery_automated")
                partner_value_cant_provide = st.text_area("What would partners value that you can't easily provide today?", value=part4a.get('partner_value_cant_provide',''), key=f"{selected_owner}-partner_value_cant_provide")
                
                st.markdown("---")
                st.markdown("**Section B: Partner Confidence & Trust**")
                partner_confidence_builders = st.text_area("What builds partner confidence in Nuton's technology?", value=part4b.get('partner_confidence_builders',''), key=f"{selected_owner}-partner_confidence_builders")
                partner_concerns = st.text_area("What concerns or questions do partners have?", value=part4b.get('partner_concerns',''), key=f"{selected_owner}-partner_concerns")
                partner_demonstrate_data_led = st.text_area("How could Nuton better demonstrate 'data-led' capability to partners?", value=part4b.get('partner_demonstrate_data_led',''), key=f"{selected_owner}-partner_demonstrate_data_led")
            
            with st.expander("Part 5: Ideal Future State - Business Requirements", expanded=False):
                st.markdown("**Section A: Prioritization Discussion**")
                priority_biggest_impact = st.text_area("If you could improve one thing, what would have the biggest business impact?", value=part5a.get('priority_biggest_impact',''), key=f"{selected_owner}-priority_biggest_impact")
                priority_why = st.text_area("Why that one?", value=part5a.get('priority_why',''), key=f"{selected_owner}-priority_why")
                priority_impact_detail = st.text_area("What would the impact be? (time saved, quality improved, etc.)", value=part5a.get('priority_impact_detail',''), key=f"{selected_owner}-priority_impact_detail")
                priority_frequency = st.text_area("How often would it help?", value=part5a.get('priority_frequency',''), key=f"{selected_owner}-priority_frequency")
                priority_prevents_faster = st.text_area("What prevents you from delivering faster with partners?", value=part5a.get('priority_prevents_faster',''), key=f"{selected_owner}-priority_prevents_faster")
                priority_partner_difference = st.text_area("What would make the biggest difference to partner confidence or satisfaction?", value=part5a.get('priority_partner_difference',''), key=f"{selected_owner}-priority_partner_difference")
                
                st.markdown("---")
                st.markdown("**Section B: Vision Discussion (12-18 months from now)**")
                st.markdown("*Imagine the Predict platform is working beautifully for you...*")
                vision_day_to_day = st.text_area("What does your day-to-day work look like?", value=part5b.get('vision_day_to_day',''), key=f"{selected_owner}-vision_day_to_day")
                vision_can_do_new = st.text_area("What can you do that you can't do today?", value=part5b.get('vision_can_do_new',''), key=f"{selected_owner}-vision_can_do_new")
                vision_decisions_faster = st.text_area("What decisions can you make faster or better?", value=part5b.get('vision_decisions_faster',''), key=f"{selected_owner}-vision_decisions_faster")
                vision_partner_delivery_changed = st.text_area("How has partner delivery changed?", value=part5b.get('vision_partner_delivery_changed',''), key=f"{selected_owner}-vision_partner_delivery_changed")
                st.markdown("**Information access**")
                vision_information_access = st.text_area("What information do you have access to that you don't today?", value=part5b.get('vision_information_access',''), key=f"{selected_owner}-vision_information_access")
                vision_questions_answer = st.text_area("What questions can you answer?", value=part5b.get('vision_questions_answer',''), key=f"{selected_owner}-vision_questions_answer")
                vision_answer_speed = st.text_area("How quickly can you get answers?", value=part5b.get('vision_answer_speed',''), key=f"{selected_owner}-vision_answer_speed")
                vision_information_confidence = st.text_area("How confident are you in the information?", value=part5b.get('vision_information_confidence',''), key=f"{selected_owner}-vision_information_confidence")
                st.markdown("**Workflow changes**")
                vision_workflow_changed = st.text_area("How has your workflow changed?", value=part5b.get('vision_workflow_changed',''), key=f"{selected_owner}-vision_workflow_changed")
                vision_manual_steps_gone = st.text_area("What manual steps are gone?", value=part5b.get('vision_manual_steps_gone',''), key=f"{selected_owner}-vision_manual_steps_gone")
                vision_whats_faster = st.text_area("What's faster?", value=part5b.get('vision_whats_faster',''), key=f"{selected_owner}-vision_whats_faster")
                vision_whats_easier = st.text_area("What's easier?", value=part5b.get('vision_whats_easier',''), key=f"{selected_owner}-vision_whats_easier")
                vision_whats_reliable = st.text_area("What's more reliable?", value=part5b.get('vision_whats_reliable',''), key=f"{selected_owner}-vision_whats_reliable")
                st.markdown("**Partner experience**")
                vision_partner_experience_faster = st.text_area("What's faster from partner perspective?", value=part5b.get('vision_partner_experience_faster',''), key=f"{selected_owner}-vision_partner_experience_faster")
                vision_partner_confidence = st.text_area("What builds their confidence?", value=part5b.get('vision_partner_confidence',''), key=f"{selected_owner}-vision_partner_confidence")
                vision_partner_access = st.text_area("What do they have access to that they don't today?", value=part5b.get('vision_partner_access',''), key=f"{selected_owner}-vision_partner_access")
                
                st.markdown("---")
                st.markdown("**Section C: Capability Requirements**")
                capability_requirements = st.text_area("What capabilities must the Predict platform provide? (I need to be able to...)", value=part5c.get('capability_requirements',''), key=f"{selected_owner}-capability_requirements")
                capability_fast_enough = st.text_area("What would 'fast enough' look like? (timeline requirements)", value=part5c.get('capability_fast_enough',''), key=f"{selected_owner}-capability_fast_enough")
                capability_quality_requirements = st.text_area("What would 'good enough' quality look like? (accuracy, confidence, validation)", value=part5c.get('capability_quality_requirements',''), key=f"{selected_owner}-capability_quality_requirements")
            
            with st.expander("Part 6: Wrap-Up (5m)", expanded=False):
                st.markdown("**Summarization and Validation**")
                summary_validation = st.text_area("Summary validation - Did I get that right?", value=part6.get('summary_validation',''), key=f"{selected_owner}-summary_validation")
                summary_missed = st.text_area("What did I miss?", value=part6.get('summary_missed',''), key=f"{selected_owner}-summary_missed")
                summary_most_important = st.text_area("What's most important?", value=part6.get('summary_most_important',''), key=f"{selected_owner}-summary_most_important")
                summary_critical_not_discussed = st.text_area("Is there anything critical we haven't talked about?", value=part6.get('summary_critical_not_discussed',''), key=f"{selected_owner}-summary_critical_not_discussed")
                summary_ensure_understanding = st.text_area("Anything you want to make sure we understand?", value=part6.get('summary_ensure_understanding',''), key=f"{selected_owner}-summary_ensure_understanding")
            
            submitted = st.form_submit_button("Save Business Owner Session")
            if submitted:
                owner_data = {
                    'owner_name': selected_owner,
                    'products_covered': [p['product_name'] for p in products_for_owner],
                    'part1_context_business_process': {
                        'context_role': context_role,
                        'context_stages': context_stages,
                        'context_decisions': context_decisions,
                        'context_deliverables': context_deliverables,
                        'context_workflow': context_workflow,
                        'context_steps': context_steps,
                        'context_info_needed': context_info_needed,
                        'context_decision_points': context_decision_points,
                        'context_partner_impact': context_partner_impact,
                        'context_partner_confidence': context_partner_confidence,
                        'context_partner_frustration': context_partner_frustration
                    },
                    'part2_product_portfolio_review': {
                        'section_a_business_owner': {
                            'product_purpose': product_purpose,
                            'product_why_created': product_why_created,
                            'product_what_achieve': product_what_achieve,
                            'product_impact_works_well': product_impact_works_well,
                            'product_impact_doesnt_work': product_impact_doesnt_work,
                            'product_time_impact': product_time_impact,
                            'product_quality_decisions': product_quality_decisions,
                            'product_partner_confidence': product_partner_confidence
                        },
                        'section_b_users': {
                            'b1_use_overview': {
                                'use_purpose': use_purpose,
                                'use_frequency': use_frequency,
                                'use_who_else': use_who_else,
                                'use_workflow_stage': use_workflow_stage,
                                'use_critical_path': use_critical_path,
                                'use_decisions': use_decisions,
                                'use_decision_explanation': use_decision_explanation,
                                'use_critical_decisions': use_critical_decisions,
                                'use_confidence_outputs': use_confidence_outputs,
                                'use_decisions_without_product': use_decisions_without_product,
                                'use_why_not_direct': use_why_not_direct
                            },
                            'b2_pain_points_gaps': {
                                'pain_frustrations': pain_frustrations,
                                'pain_slowdowns': pain_slowdowns,
                                'pain_extra_work': pain_extra_work,
                                'pain_rework_errors': pain_rework_errors,
                                'pain_unsupported_needs': pain_unsupported_needs,
                                'pain_content_quality': pain_content_quality,
                                'pain_timeline': pain_timeline,
                                'pain_usability': pain_usability,
                                'pain_missing_info': pain_missing_info,
                                'pain_missing_decisions': pain_missing_decisions,
                                'pain_manual_work': pain_manual_work,
                                'pain_workarounds': pain_workarounds,
                                'pain_time_added': pain_time_added,
                                'pain_why_necessary': pain_why_necessary
                            }
                        }
                    },
                    'part3_cross_product_process': {
                        'section_a_integration': {
                            'integration_products_work_together': integration_products_work_together,
                            'integration_manual_data_movement': integration_manual_data_movement,
                            'integration_gaps': integration_gaps,
                            'integration_combine_info': integration_combine_info,
                            'integration_how_combine': integration_how_combine,
                            'integration_time_to_combine': integration_time_to_combine,
                            'integration_error_prone': integration_error_prone,
                            'integration_outside_products': integration_outside_products,
                            'integration_outside_fit': integration_outside_fit
                        },
                        'section_b_bottlenecks': {
                            'bottleneck_where_slows': bottleneck_where_slows,
                            'bottleneck_waiting_info': bottleneck_waiting_info,
                            'bottleneck_manual_steps': bottleneck_manual_steps,
                            'bottleneck_rework': bottleneck_rework,
                            'bottleneck_handoffs': bottleneck_handoffs,
                            'bottleneck_takes_longer': bottleneck_takes_longer,
                            'bottleneck_why_long': bottleneck_why_long,
                            'bottleneck_faster_look_like': bottleneck_faster_look_like,
                            'bottleneck_partner_delays': bottleneck_partner_delays,
                            'bottleneck_partner_waiting': bottleneck_partner_waiting,
                            'bottleneck_partner_frustrations': bottleneck_partner_frustrations
                        }
                    },
                    'part4_partner_delivery': {
                        'section_a_info_needs': {
                            'partner_info_needs': partner_info_needs,
                            'partner_info_frequency': partner_info_frequency,
                            'partner_info_format': partner_info_format,
                            'partner_delivery_method': partner_delivery_method,
                            'partner_delivery_time': partner_delivery_time,
                            'partner_delivery_automated': partner_delivery_automated,
                            'partner_value_cant_provide': partner_value_cant_provide
                        },
                        'section_b_confidence_trust': {
                            'partner_confidence_builders': partner_confidence_builders,
                            'partner_concerns': partner_concerns,
                            'partner_demonstrate_data_led': partner_demonstrate_data_led
                        }
                    },
                    'part5_ideal_future_state': {
                        'section_a_prioritization': {
                            'priority_biggest_impact': priority_biggest_impact,
                            'priority_why': priority_why,
                            'priority_impact_detail': priority_impact_detail,
                            'priority_frequency': priority_frequency,
                            'priority_prevents_faster': priority_prevents_faster,
                            'priority_partner_difference': priority_partner_difference
                        },
                        'section_b_vision': {
                            'vision_day_to_day': vision_day_to_day,
                            'vision_can_do_new': vision_can_do_new,
                            'vision_decisions_faster': vision_decisions_faster,
                            'vision_partner_delivery_changed': vision_partner_delivery_changed,
                            'vision_information_access': vision_information_access,
                            'vision_questions_answer': vision_questions_answer,
                            'vision_answer_speed': vision_answer_speed,
                            'vision_information_confidence': vision_information_confidence,
                            'vision_workflow_changed': vision_workflow_changed,
                            'vision_manual_steps_gone': vision_manual_steps_gone,
                            'vision_whats_faster': vision_whats_faster,
                            'vision_whats_easier': vision_whats_easier,
                            'vision_whats_reliable': vision_whats_reliable,
                            'vision_partner_experience_faster': vision_partner_experience_faster,
                            'vision_partner_confidence': vision_partner_confidence,
                            'vision_partner_access': vision_partner_access
                        },
                        'section_c_capabilities': {
                            'capability_requirements': capability_requirements,
                            'capability_fast_enough': capability_fast_enough,
                            'capability_quality_requirements': capability_quality_requirements
                        }
                    },
                    'part6_wrapup': {
                        'summary_validation': summary_validation,
                        'summary_missed': summary_missed,
                        'summary_most_important': summary_most_important,
                        'summary_critical_not_discussed': summary_critical_not_discussed,
                        'summary_ensure_understanding': summary_ensure_understanding
                    }
                }
                save_business_owner_data(selected_owner, owner_data)
                st.success(f"Business Owner data saved for {selected_owner} ✅")
                st.rerun()

    elif page == 'Export Backup':
        st.header("Backup & Restore")
        aggregated = load_aggregated_data()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Export Backup")
            backup_str = json.dumps(aggregated, indent=2)
            fname = f"aggregated-backup-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
            st.download_button("Download Backup (JSON)", backup_str, file_name=fname, mime="application/json")
        with col2:
            st.subheader("Restore Backup")
            uploaded = st.file_uploader("Select backup JSON to restore", type=["json"], key="restore_backup")
            if uploaded is not None:
                try:
                    content = uploaded.read().decode("utf-8")
                    data = json.loads(content)
                    # Basic validation
                    if not isinstance(data, dict) or 'products' not in data or 'business_owners' not in data:
                        st.error("Invalid backup format: expected keys 'products' and 'business_owners'.")
                    else:
                        save_aggregated_data(data)
                        st.success("Backup restored to aggregated.json")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to load backup: {e}")

    elif page == "Products":
        st.header("Products (latest session only)")
        products = load_products()
        if not products:
            st.info("No products found yet. Create a session for a product in 'Create Session'.")
        else:
            product_filter = st.text_input("Filter by product")
            displayed = [p for p in products if (not product_filter) or (product_filter.lower() in (p.get('product_name') or '').lower())]

            st.markdown("**Products**")
            for p in displayed:
                cols = st.columns([1, 5, 2, 1])
                cols[0].write(p.get('product_id'))
                cols[1].write(f"**{p.get('product_name')}**")
                if cols[2].button("View", key=f"view-{p.get('product_id')}"):
                    st.session_state['selected_product'] = p.get('product_id')
                    # move to Edit mode so the Create/Edit form is shown
                    st.session_state['app_mode'] = 'Edit mode'
                    st.rerun()
                if cols[3].button("Edit", key=f"edit-{p.get('product_id')}"):
                    st.session_state['editing_product'] = p.get('product_id')
                    st.session_state['app_mode'] = 'Edit mode'
                    st.rerun()

            # If a product was selected for viewing, show its data
            selected_pid = st.session_state.get('selected_product')
            if selected_pid:
                product_data = get_product_data(selected_pid)
                st.subheader(f"Product: {product_data.get('product_name', selected_pid)}")
                
                if product_data:
                    st.markdown("### Product Information")
                    st.write(f"**Business Owner:** {product_data.get('business_owner', 'N/A')}")
                    st.write(f"**Workstream:** {product_data.get('workstream', 'N/A')}")
                    st.write(f"**Primary Operator:** {product_data.get('primary_operator', 'N/A')}")
                    st.write(f"**Primary Developer:** {product_data.get('primary_developer', 'N/A')}")
                    # No timestamp stored
                    
                    st.download_button("Download Product JSON", json.dumps(product_data, indent=2), file_name=f"{selected_pid}-data.json")
                else:
                    st.info("No data recorded for this product yet.")

    elif page == "Export All":
        st.header("Export All Products")
        products = load_products()
        if not products:
            st.info("No products to export.")
        else:
            df = pd.DataFrame(products)
            st.download_button("Download All Products CSV", df.to_csv(index=False), file_name="all-products.csv")
            st.dataframe(df)


if __name__ == '__main__':
    main()
