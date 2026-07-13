.PHONY: install dev build export

install:
	pnpm install

dev:
	pnpm exec slidev --open --force

dev-host:
	pnpm exec slidev --open --remote --force

build:
	pnpm exec slidev build

export:
	pnpm exec slidev export
