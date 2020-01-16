import psutil
import json
import click


@click.command()
@click.argument('file', type=click.File('a'), default='data.json')
def process(file):
    print('Checking process')
    f = file
    for p in psutil.process_iter():
        if p.memory_percent() > 5:
            print(p.cpu_percent(0.1))
            f.write(json.dumps(p.as_dict(), default=str)+'\n')


if __name__ == "__main__":
    #f = open('data.json')
    #process()
