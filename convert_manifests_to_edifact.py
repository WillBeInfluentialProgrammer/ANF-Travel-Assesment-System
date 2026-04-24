#!/usr/bin/env python3
"""
Excel Manifest to EDIFACT PAXLST Converter
Based on the actual Excel format with columns: No, CIS, Surname, Name, TO, Seat, G, CC, Ssr, NAT, DOC, DOB, P/W
"""

import pandas as pd
from datetime import datetime
import os
import sys

def parse_date(date_str):
    """Parse date from Excel format to YYMMDD"""
    if pd.isna(date_str):
        return ""
    
    # If it's already a datetime object
    if isinstance(date_str, datetime):
        return date_str.strftime("%y%m%d")
    
    date_str = str(date_str).strip()
    
    # Try different date formats
    formats = [
        "%d-%b-%y",  # 11-Mar-84
        "%d-%b-%Y",  # 11-Mar-1984
        "%d/%m/%y",  # 11/03/84
        "%d/%m/%Y",  # 11/03/1984
        "%m/%d/%Y",  # 03/11/1984
        "%Y-%m-%d",  # 1984-03-11
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%y%m%d")
        except:
            continue
    
    # If no format works, try to extract just numbers
    numbers = ''.join(filter(str.isdigit, date_str))
    if len(numbers) >= 6:
        return numbers[-6:]  # Take last 6 digits
    
    return ""

def clean_string(s):
    """Clean string for EDIFACT format"""
    if pd.isna(s):
        return ""
    return str(s).strip().upper().replace('*', '').replace(':', '').replace('$', '').replace('?', '')

def convert_manifest_to_edifact(excel_file, flight_num, origin, dest, departure_time, arrival_time):
    """
    Convert Excel manifest to EDIFACT format
    
    Args:
        excel_file: Path to Excel file
        flight_num: Flight number (e.g., "PK233")
        origin: Origin airport code (e.g., "ISB")
        dest: Destination airport code (e.g., "DXB")
        departure_time: Departure time as "YYMMDDHHMM"
        arrival_time: Arrival time as "YYMMDDHHMM"
    """
    
    print(f"\nProcessing: {os.path.basename(excel_file)}")
    print(f"Flight: {flight_num} from {origin} to {dest}")
    
    # Read Excel file - skip first row if it contains header info
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
    # Find the row with column headers (contains "Surname", "Name", etc.)
    header_row = None
    for idx, row in df.iterrows():
        row_str = ' '.join([str(val) for val in row.values if not pd.isna(val)])
        if 'Surname' in row_str and 'Name' in row_str:
            header_row = idx
            break
    
    if header_row is not None:
        # Re-read with proper header
        df = pd.read_excel(excel_file, skiprows=header_row)
    
    # Generate message reference
    now = datetime.now()
    msg_date = now.strftime("%y%m%d")
    msg_time = now.strftime("%H%M")
    msg_ref = now.strftime("%y%m%d%H%M%S00001")
    
    # Build EDIFACT message
    lines = []
    
    # UNA - Service String Advice
    lines.append("UNA:*.? $")
    
    # UNB - Interchange Header
    lines.append(f"UNB*UNOA:4*PIA:ZZ*GTAS:ZZ*{msg_date}:{msg_time}*{msg_ref}**APIS$")
    
    # UNG - Group Header
    lines.append(f"UNG*PAXLST*PIA:ZZ*GTAS:ZZ*{msg_date}:{msg_time}*{msg_ref}*UN*D:02B$")
    
    # UNH - Message Header
    lines.append(f"UNH*{msg_ref}*PAXLST:D:02B:UN:IATA*{flight_num}*01:F$")
    
    # BGM - Beginning of Message
    lines.append("BGM*745$")
    
    # TDT - Transport Details
    lines.append(f"TDT*20*{flight_num}$")
    
    # LOC - Origin
    lines.append(f"LOC*125*{origin}$")
    lines.append(f"DTM*189:{departure_time}:201$")
    
    # LOC - Destination  
    lines.append(f"LOC*87*{dest}$")
    lines.append(f"DTM*232:{arrival_time}:201$")
    
    # Process each passenger
    passenger_count = 0
    
    for idx, row in df.iterrows():
        # Extract No, CIS, Surname from first column (format: "001 35 AHMAD")
        no_cis_surname = str(row.get('No  CIS  Surname', ''))
        parts = no_cis_surname.strip().split()
        
        # Parse: No (001), CIS (35), Surname (AHMAD)
        if len(parts) >= 3:
            pax_no = parts[0]
            cis = parts[1]
            surname = clean_string(' '.join(parts[2:]))  # Join remaining parts as surname
        elif len(parts) == 2:
            pax_no = parts[0]
            cis = ""
            surname = clean_string(parts[1])
        elif len(parts) == 1:
            pax_no = ""
            cis = ""
            surname = clean_string(parts[0])
        else:
            continue  # Skip empty rows
        
        # Get first name from "Name" column
        name = clean_string(row.get('Name', ''))
        
        if not surname and not name:
            continue
        
        # Extract passenger data
        gender = clean_string(row.get('G', 'M'))
        if gender not in ['M', 'F']:
            gender = 'M'
        
        nationality = clean_string(row.get('NAT', 'PAK'))
        if not nationality:
            nationality = 'PAK'
        
        doc_number = clean_string(row.get('DOC', ''))
        if not doc_number:
            continue  # Skip passengers without passport
        
        dob = parse_date(row.get('DOB', ''))
        passport_expiry = parse_date(row.get('P/W', ''))
        
        # Generate PNR
        pnr = f"PNR{passenger_count:06d}"
        
        # NAD - Passenger name
        lines.append(f"NAD*FL***{surname}:{name}:$")
        
        # ATT - Passenger type and gender
        lines.append(f"ATT*2**{gender}$")
        
        # DTM - Date of birth
        if dob:
            lines.append(f"DTM*329:{dob}$")
        
        # LOC - Origin/Destination for passenger
        lines.append(f"LOC*178*{origin}$")
        lines.append(f"LOC*179*{dest}$")
        
        # NAT - Nationality
        lines.append(f"NAT*2*{nationality}$")
        
        # RFF - Reservation reference
        lines.append(f"RFF*AVF:{pnr}$")
        
        # DOC - Travel document
        lines.append(f"DOC*P:110:111*{doc_number}$")
        
        # DTM - Document expiry
        if passport_expiry:
            lines.append(f"DTM*36:{passport_expiry}$")
        else:
            # Default expiry 5 years from now
            default_expiry = datetime.now().replace(year=datetime.now().year + 5).strftime("%y%m%d")
            lines.append(f"DTM*36:{default_expiry}$")
        
        # LOC - Document issuing country
        lines.append(f"LOC*91*{nationality}$")
        
        passenger_count += 1
    
    # CNT - Control totals
    lines.append(f"CNT*42:{passenger_count}$")
    
    # UNT - Message Trailer
    segment_count = len(lines) - 3  # Exclude UNA, UNB, UNG
    lines.append(f"UNT*{segment_count + 1}*{msg_ref}$")
    
    # UNE - Group Trailer
    lines.append(f"UNE*1*{msg_ref}$")
    
    # UNZ - Interchange Trailer
    lines.append(f"UNZ*1*{msg_ref}$")
    
    print(f"✓ Converted {passenger_count} passengers")
    
    return '\n'.join(lines), passenger_count, flight_num

def main():
    """Main conversion function"""
    
    base_dir = r"c:\Users\admain\Desktop\GTAS-S-master\GTAS-master"
    excel_folder = os.path.join(base_dir, "excel files")
    output_folder = os.path.join(base_dir, "gtas-data", "input")
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Define manifests to convert with their flight details
    manifests = [
        {
            'file': 'PK233 MANIFEST EXCEL.xlsx',
            'flight': 'PK233',
            'origin': 'ISB',
            'dest': 'DXB',
            'departure': '2512161200',  # Dec 16, 2025 12:00
            'arrival': '2512161700'      # Dec 16, 2025 17:00
        },
        {
            'file': 'PK143 MANIFEST EXCEL.xlsx',
            'flight': 'PK143',
            'origin': 'ISB',
            'dest': 'AAN',
            'departure': '2512161200',
            'arrival': '2512161700'
        },
        {
            'file': 'PK287 MANIFEST EXCEL.xlsx',
            'flight': 'PK287',
            'origin': 'ISB',
            'dest': 'LHE',
            'departure': '2512161400',
            'arrival': '2512161600'
        },
        {
            'file': 'pk841 manifest excel.xlsx',
            'flight': 'PK841',
            'origin': 'LHE',
            'dest': 'KHI',
            'departure': '2512161700',
            'arrival': '2512161900'
        }
    ]
    
    print("=" * 70)
    print("Excel Manifest to EDIFACT PAXLST Converter")
    print("=" * 70)
    
    total_passengers = 0
    
    for manifest in manifests:
        excel_path = os.path.join(excel_folder, manifest['file'])
        
        if not os.path.exists(excel_path):
            print(f"\n✗ File not found: {manifest['file']}")
            continue
        
        try:
            edifact_content, pax_count, flight_num = convert_manifest_to_edifact(
                excel_path,
                manifest['flight'],
                manifest['origin'],
                manifest['dest'],
                manifest['departure'],
                manifest['arrival']
            )
            
            if edifact_content:
                # Save to file
                output_filename = f"{flight_num}_apis.edi"
                output_path = os.path.join(output_folder, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(edifact_content)
                
                print(f"✓ Saved: {output_filename}")
                total_passengers += pax_count
                
        except Exception as e:
            print(f"\n✗ Error processing {manifest['file']}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"Conversion Complete!")
    print(f"Total passengers: {total_passengers}")
    print(f"Output folder: {output_folder}")
    print("=" * 70)

if __name__ == "__main__":
    main()
