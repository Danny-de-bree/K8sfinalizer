import click

@click.command()
@click.option('--namespace', help='Namespace to use')
def main(namespace):
    click.echo(click.style('Welcome to the tool that will help you delete annoying terminating namespaces', fg='green', bold=True))
    click.echo(click.style(f'Using namespace: {namespace}', fg='red'))
    
if __name__ == '__main__':
    main()