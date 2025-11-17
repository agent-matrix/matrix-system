"""
Main CLI entrypoint for Matrix System.

This module provides the command-line interface for interacting
with Matrix System services using Typer.
"""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from matrix_system import __version__
from matrix_system.api.client import MatrixClient
from matrix_system.api.exceptions import MatrixAPIError
from matrix_system.utils.config import get_config
from matrix_system.utils.logger import get_logger, setup_logging

app = typer.Typer(
    name="matrix",
    help="Matrix System - The First Alive AI Platform CLI",
    add_completion=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """
    Print version and exit.

    Args:
        value: If True, print version and exit
    """
    if value:
        console.print(f"Matrix System version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
    json_logs: bool = typer.Option(
        False,
        "--json-logs",
        help="Output logs in JSON format",
    ),
) -> None:
    """
    Matrix System CLI - Interact with the Agent-Matrix ecosystem.

    Args:
        version: Show version and exit
        log_level: Logging level
        json_logs: Enable JSON log format
    """
    setup_logging(log_level=log_level, json_format=json_logs)


@app.command()
def health(
    service: str = typer.Option(
        "hub",
        "--service",
        "-s",
        help="Service to check (hub, ai, guardian, all)",
    ),
) -> None:
    """
    Check health of Matrix services.

    Args:
        service: Which service to check
    """
    logger = get_logger(__name__)
    config = get_config()

    console.print(f"[bold blue]Checking health of {service}...[/bold blue]")

    services_to_check = (
        ["hub", "ai", "guardian"] if service == "all" else [service]
    )

    table = Table(title="Matrix System Health")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Response Time", style="yellow")

    with MatrixClient(config=config) as client:
        for svc in services_to_check:
            try:
                import time

                start = time.time()
                result = client.health_check(svc)
                duration = round((time.time() - start) * 1000, 2)

                status = result.get("status", "unknown")
                table.add_row(
                    svc.upper(),
                    f"✓ {status}",
                    f"{duration}ms",
                )
                logger.info(
                    "health_check_success",
                    service=svc,
                    status=status,
                    duration_ms=duration,
                )

            except MatrixAPIError as e:
                table.add_row(
                    svc.upper(),
                    f"✗ {str(e)}",
                    "N/A",
                )
                logger.error("health_check_failed", service=svc, error=str(e))

    console.print(table)


@app.command()
def info() -> None:
    """Display Matrix System information and configuration."""
    config = get_config()

    console.print("\n[bold blue]Matrix System Information[/bold blue]\n")

    info_table = Table(show_header=False, box=None)
    info_table.add_column("Key", style="cyan")
    info_table.add_column("Value", style="green")

    info_table.add_row("Version", __version__)
    info_table.add_row("Matrix Hub URL", str(config.matrix_hub_url))
    info_table.add_row("Matrix AI URL", str(config.matrix_ai_url))
    info_table.add_row("Matrix Guardian URL", str(config.matrix_guardian_url))
    info_table.add_row("Timeout", f"{config.timeout}s")
    info_table.add_row("Max Retries", str(config.max_retries))
    info_table.add_row("Log Level", config.log_level)
    info_table.add_row(
        "API Token",
        "Configured" if config.api_token else "Not configured",
    )

    console.print(info_table)
    console.print()


@app.command()
def events(
    limit: int = typer.Option(
        10,
        "--limit",
        "-n",
        help="Number of events to display",
    ),
    app_uid: Optional[str] = typer.Option(
        None,
        "--app",
        "-a",
        help="Filter by application UID",
    ),
) -> None:
    """
    Display recent Matrix System events.

    Args:
        limit: Number of events to display
        app_uid: Filter by application UID
    """
    console.print(
        f"[bold yellow]Fetching last {limit} events...[/bold yellow]"
    )
    console.print("[dim]Note: This is a placeholder. Implement API integration.[/dim]")


@app.command()
def proposals(
    state: Optional[str] = typer.Option(
        None,
        "--state",
        "-s",
        help="Filter by state (pending, approved, rejected)",
    ),
) -> None:
    """
    Display Matrix System proposals.

    Args:
        state: Filter by proposal state
    """
    console.print("[bold yellow]Fetching proposals...[/bold yellow]")
    console.print("[dim]Note: This is a placeholder. Implement API integration.[/dim]")


def cli_main() -> None:
    """Entrypoint for the CLI."""
    app()


if __name__ == "__main__":
    cli_main()
