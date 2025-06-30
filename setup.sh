# ModCore - UserBot (Pyrogram Version)
# Copyright (C) 2025 aesneverhere

#!/bin/bash

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}🔧 Setup mulai...${NC}"

if [ -f "config.py" ]; then
    echo -e "${GREEN}✅ config.py udah ada, lewatin...${NC}"
else
    cp config_sample.py config.py
    echo -e "${GREEN}✅ config.py dibuat dari template!${NC}"
fi

if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Install requirements...${NC}"
    pip install -r requirements.txt
else
    echo -e "${RED}❌ requirements.txt hilang!${NC}"
    exit 1
fi

echo -e "${YELLOW}🧵 Generate session string...${NC}"
python3 generate_session.py

echo -e "${GREEN}✅ Setup selesai! Langsung bisa run pakai ./run.sh 🔥${NC}"
