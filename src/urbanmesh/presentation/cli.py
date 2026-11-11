"""Local utility commands for operators."""
import argparse, json
from datetime import date
from urbanmesh.bootstrap import build_services

def main():
    parser=argparse.ArgumentParser(prog="urbanmesh")
    parser.add_argument("command",choices=["routes","inventory","stations","ridership"])
    args=parser.parse_args()
    services=build_services()
    if args.command=="routes": values=[r.route_id for r in services.routes_store.all_routes()]
    elif args.command=="inventory": values=[x.sku for x in services.inventory.list()]
    elif args.command=="stations": values=[x.bike_id for x in services.bikes_store.available_at("CENTRO")]
    else: values=services.ridership.build(date.today())
    print(json.dumps(values,ensure_ascii=False))

if __name__=="__main__":main()
